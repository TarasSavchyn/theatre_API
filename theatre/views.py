from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Play, Genre, Actor, TheatreHall, Performance, Reservation, Ticket
from .serializers import (
    PlaySerializer,
    GenreSerializer,
    ActorSerializer,
    TheatreHallSerializer,
    PerformanceSerializer,
    ReservationSerializer,
    TicketSerializer,
    PerformanceListSerializer,
    PerformanceDetailSerializer,
    PlayListSerializer,
    PlayDetailSerializer,
    ReservationListSerializer,
    ReservationDetailSerializer,
)


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()

    def get_queryset(self):
        queryset = Play.objects.all()

        # filtering by genres
        genres = self.request.query_params.get("genres")
        if genres:
            genres_ids = [int(str_id) for str_id in genres.split(",")]
            queryset = Play.objects.filter(genres__id__in=genres_ids)

            for genre_id in genres_ids:
                queryset = queryset.filter(genres__id=genre_id)

        # filtering by actors
        actors = self.request.query_params.get("actors")
        if actors:
            actors_ids = [int(str_id) for str_id in actors.split(",")]
            queryset = Play.objects.filter(actors__id__in=actors_ids)

            for actor_id in actors_ids:
                queryset = queryset.filter(actors__id=actor_id)

        return queryset.distinct()



    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer

        if self.action == "retrieve":
            return PlayDetailSerializer

        return PlaySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_queryset(self):
        queryset = Genre.objects.all()

        # filtering by name
        name = self.request.query_params.get("name")

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class TheatreHallViewSet(viewsets.ModelViewSet):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer

        if self.action == "retrieve":
            return PerformanceDetailSerializer

        return PerformanceSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer

        if self.action == "retrieve":
            return ReservationDetailSerializer

        return ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["POST"])
    def cancel_reservation(self, request, pk=None):
        reservation = self.get_object()
        reservation.status = False
        reservation.save()
        return Response({"message": "Reservation has been canceled."})
