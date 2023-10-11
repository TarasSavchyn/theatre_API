import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        ordering = [
            "name",
        ]


def actor_foto_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.full_name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/theater/", filename)


class Actor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    foto = models.ImageField(upload_to=actor_foto_file_path, null=True, blank=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ["first_name", "last_name"]


class Play(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)

    def __str__(self):
        return self.title

    class Meta:
        ordering = [
            "title",
        ]


class TheatreHall(models.Model):
    name = models.CharField(max_length=100)
    rows = models.PositiveIntegerField()
    seats_in_row = models.PositiveIntegerField()

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name

    class Meta:
        ordering = [
            "name",
        ]


class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE)
    theatre_hall = models.ForeignKey(TheatreHall, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    @property
    def available_tickets(self):
        reserved_tickets = self.ticket_set.filter(reservation__status=True).count()
        total_tickets = self.theatre_hall.capacity
        return total_tickets - reserved_tickets

    def __str__(self):
        return f"{self.play.title} at {self.theatre_hall.name}, {self.show_time}"

    class Meta:
        ordering = [
            "show_time",
        ]


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = [
            "created_at",
        ]

    def __str__(self):
        return f"Reservation by {self.user.username}"


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name="tickets",
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"Ticket for {self.performance.play.title}, Row {self.row}, Seat {self.seat}"

    class Meta:
        # unique_together = ("performance", "row", "seat")
        ordering = ["row", "seat"]
