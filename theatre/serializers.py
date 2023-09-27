from rest_framework import serializers
from .models import Play, Genre, Actor, TheatreHall, Performance, Reservation, Ticket

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

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
        fields = '__all__'


class PlayListSerializer(PlaySerializer):
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )
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
    theatre_hall_capacity = serializers.IntegerField(source="theatre_hall.capacity", read_only=True)
    theatre_hall_name = serializers.CharField(source="theatre_hall.name", read_only=True)

    class Meta:
        model = Performance
        fields = [
            "id",
            "play_title",
            "theatre_hall_capacity",
            "available_tickets",
            "theatre_hall_name",
            "show_time",
        ]

class PerformanceDetailSerializer(PerformanceSerializer):
    play = PlayListSerializer(many=False, read_only=True)
    theatre_hall = TheatreHallSerializer(many=False, read_only=True)


    class Meta:
        model = Performance
        fields = ["id", "play", "theatre_hall", "show_time", "available_tickets"]






class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
