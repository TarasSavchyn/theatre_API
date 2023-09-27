from rest_framework import serializers
from .models import Play, Genre, Actor, TheatreHall, Performance, Reservation, Ticket

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'


# class ActorFotoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Actor
#         fields = ("id", 'foto', )


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = '__all__'

class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = '__all__'

class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = '__all__'

class PerformanceListSerializer(serializers.ModelSerializer):
    play_title = serializers.CharField(source="play.title", read_only=True)
    theatre_hall_capacity = serializers.IntegerField(source="theatre_hall.capacity", read_only=True)
    theatre_hall_name = serializers.CharField(source="theatre_hall.name", read_only=True)

    class Meta:
        model = Performance
        fields = [
            "id",
            "play_title",
            "theatre_hall_capacity",
            "theatre_hall_name",
            "show_time",
        ]

class PerformanceDetailSerializer(PerformanceSerializer):
    play = PlaySerializer(many=False, read_only=True)
    theatre_hall = TheatreHallSerializer(many=False, read_only=True)

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
