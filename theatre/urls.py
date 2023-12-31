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

router.register(r"plays", PlayViewSet)
router.register(r"genres", GenreViewSet)
router.register(r"actors", ActorViewSet)
router.register(r"theatrehalls", TheatreHallViewSet)
router.register(r"performances", PerformanceViewSet)
router.register(r"reservations", ReservationViewSet)


urlpatterns = router.urls

app_name = "theatre"
