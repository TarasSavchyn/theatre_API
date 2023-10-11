from django.urls import path
from rest_framework import routers

from theatre.views import (
    PlayViewSet,
    GenreViewSet,
    ActorViewSet,
    TheatreHallViewSet,
    PerformanceViewSet,
    ReservationViewSet,
)

router = routers.DefaultRouter()

router.register(r'plays', PlayViewSet)
router.register(r'genres', GenreViewSet)
router.register(r'actors', ActorViewSet)
router.register(r'theatrehalls', TheatreHallViewSet)
router.register(r'performances', PerformanceViewSet)
router.register(r'reservations', ReservationViewSet)

urlpatterns = [
    path(
        'reservations/<int:pk>/cancel/',
        ReservationViewSet.as_view({'post': 'cancel_reservation'}),
        name='reservation-cancel'),
              ] + router.urls

app_name = "theatre"

