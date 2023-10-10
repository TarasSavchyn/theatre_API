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
    TicketSerializer, PerformanceListSerializer, PerformanceDetailSerializer, PlayListSerializer, PlayDetailSerializer,
    ReservationListSerializer,
)

class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer

        if self.action == "retrieve":
            return PlayDetailSerializer

        return PlaySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

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

        # if self.action == "retrieve":
        #     return ReservationDetailSerializer

        return ReservationSerializer

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['POST'])
    def cancel_reservation(self, request, pk=None):
        reservation = self.get_object()
        reservation.status = False
        reservation.save()
        return Response({"message": "Reservation has been canceled."})

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
