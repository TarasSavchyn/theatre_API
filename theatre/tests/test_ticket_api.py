from django.test import TestCase
from theatre.models import Ticket, Reservation, Performance, TheatreHall, Play
from django.contrib.auth import get_user_model
from datetime import datetime


class TicketModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("test@test.ua", "test123")
        self.play = Play.objects.create(title="Test Play", description="A test play")
        self.theatre_hall = TheatreHall.objects.create(
            name="Main Hall", rows=10, seats_in_row=12
        )
        self.performance = Performance.objects.create(
            play=self.play, theatre_hall=self.theatre_hall, show_time=datetime.now()
        )
        self.reservation = Reservation.objects.create(user=self.user)
        self.ticket = Ticket.objects.create(
            reservation=self.reservation, performance=self.performance, seat=1, row=1
        )

    def test_read_ticket(self):
        """
        Test reading a Ticket.
        """
        ticket = Ticket.objects.get(id=self.ticket.id)
        self.assertEqual(ticket.reservation.user.email, "test@test.ua")
        self.assertEqual(ticket.performance.play.title, "Test Play")
        self.assertEqual(ticket.performance.theatre_hall.name, "Main Hall")
        self.assertEqual(ticket.seat, 1)
        self.assertEqual(ticket.row, 1)

    def test_update_ticket(self):
        """
        Test updating a Ticket.
        """
        self.ticket.seat = 5
        self.ticket.row = 2
        self.ticket.save()
        updated_ticket = Ticket.objects.get(id=self.ticket.id)
        self.assertEqual(updated_ticket.seat, 5)
        self.assertEqual(updated_ticket.row, 2)

    def test_delete_ticket(self):
        """
        Test deleting a Ticket.
        """
        self.ticket.delete()
        with self.assertRaises(Ticket.DoesNotExist):
            Ticket.objects.get(id=self.ticket.id)

    def test_str_representation(self):
        """
        Test the string representation of a Ticket.
        """
        expected_str = f"Ticket for {self.performance.play.title}, Row {self.ticket.row}, Seat {self.ticket.seat}"
        self.assertEqual(str(self.ticket), expected_str)
