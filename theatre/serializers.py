from django.db import transaction
from rest_framework import serializers
from .models import Play, Genre, Actor, TheatreHall, Performance, Reservation, Ticket


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["id", "first_name", "last_name", "full_name", "foto"]


# class ActorFotoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Actor
#         fields = ("id", 'foto', )


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "title", "description", "genres", "actors")


class PlayListSerializer(PlaySerializer):
    genres = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    actors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name",
    )


class PlayDetailSerializer(PlaySerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ["id", "name", "rows", "seats_in_row", "capacity"]


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ["id", "play", "theatre_hall", "show_time"]


class PerformanceListSerializer(serializers.ModelSerializer):
    play_title = serializers.CharField(source="play.title", read_only=True)
    theatre_hall_capacity = serializers.IntegerField(
        source="theatre_hall.capacity", read_only=True
    )
    theatre_hall_name = serializers.CharField(
        source="theatre_hall.name", read_only=True
    )
    available_tickets = serializers.CharField(read_only=True)

    class Meta:
        model = Performance
        fields = [
            "id",
            "play_title",
            "theatre_hall_capacity",
            "theatre_hall_name",
            "show_time",
            "available_tickets",
        ]


class PerformanceDetailSerializer(PerformanceSerializer):
    play = PlayListSerializer(many=False, read_only=True)
    theatre_hall = TheatreHallSerializer(many=False, read_only=True)
    available_tickets = serializers.IntegerField(read_only=True)

    class Meta:
        model = Performance
        fields = ["id", "play", "theatre_hall", "show_time", "available_tickets"]


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "performance", "reservation")

    def validate(self, data):
        performance = data["performance"]
        row = data["row"]
        seat = data["seat"]

        # checking Invalid row or seat values
        theatre_hall = TheatreHall.objects.get(pk=performance.theatre_hall_id)

        if (
            row < 1
            or seat < 1
            or row > theatre_hall.rows
            or seat > theatre_hall.seats_in_row
        ):
            raise serializers.ValidationError("Invalid row or seat values")

        # checking booked places
        existing_tickets = Ticket.objects.filter(
            performance=performance, row=row, seat=seat, reservation__status=True
        )

        if existing_tickets.exists():
            raise serializers.ValidationError("This place is already booked")

        return data


class TicketListSerializer(serializers.ModelSerializer):
    performance_name = serializers.CharField(
        source="performance.play.title", read_only=True
    )
    performance_hall = serializers.CharField(
        source="performance.theatre_hall.name", read_only=True
    )

    class Meta:
        model = Ticket
        fields = ("id", "performance_name", "performance_hall", "row", "seat")


class TicketDetailSerializer(serializers.ModelSerializer):
    performance = PerformanceSerializer(many=False, read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "performance", "row", "seat")


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=False)

    class Meta:
        model = Reservation
        fields = ("id", "tickets", "created_at")


    @transaction.atomic
    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets", [])

        reservation = Reservation.objects.create(**validated_data)

        for ticket_data in tickets_data:
            performance = ticket_data["performance"]
            performance_id = performance.id  # Отримати ID вистави з об'єкта вистави
            Ticket.objects.create(
                reservation=reservation, performance_id=performance_id, **ticket_data
            )

        return reservation


class ReservationListSerializer(serializers.ModelSerializer):
    tickets = TicketListSerializer(read_only=True, many=True)

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "status", "tickets")


class ReservationDetailSerializer(serializers.ModelSerializer):
    tickets = TicketDetailSerializer(read_only=True, many=True)

    class Meta:
        model = Reservation
        fields = ("id", "created_at", "user", "status", "tickets")
