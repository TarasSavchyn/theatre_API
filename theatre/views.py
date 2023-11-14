from datetime import date

from rest_framework.permissions import IsAdminUser, IsAuthenticated

from django.db.models import Q
from drf_spectacular.utils import OpenApiParameter, extend_schema

from rest_framework.exceptions import ParseError
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Play,
    Genre,
    Actor,
    TheatreHall,
    Performance,
    Reservation,
    Rating,
)
from .serializers import (
    PlaySerializer,
    GenreSerializer,
    ActorSerializer,
    TheatreHallSerializer,
    PerformanceSerializer,
    ReservationSerializer,
    PerformanceListSerializer,
    PerformanceDetailSerializer,
    PlayListSerializer,
    PlayDetailSerializer,
    ReservationListSerializer,
    ReservationDetailSerializer,
    ActorFotoSerializer,
    ActorListSerializer,
    ActorDetailSerializer,
    SetRatingSerializer,
)


class PlayViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Play.objects.all()

    def get_queryset(self):
        queryset = Play.objects.all()

        # filtering by genres
        genres = self.request.query_params.get("genres")
        if genres:
            genres_ids = [int(str_id) for str_id in genres.split(",")]
            queryset = Play.objects.filter(genres__id__in=genres_ids)

        # filtering by actors
        actors = self.request.query_params.get("actors")
        if actors:
            actors_ids = [int(str_id) for str_id in actors.split(",")]
            queryset = Play.objects.filter(actors__id__in=actors_ids)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer

        if self.action == "retrieve":
            return PlayDetailSerializer

        if self.action == "evaluate":
            return SetRatingSerializer

        return PlaySerializer

    @action(
        detail=True,
        methods=["POST"],
        serializer_class=SetRatingSerializer,
        url_path="evaluate",
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def evaluate(self, request, pk=None):
        try:
            mark = float(request.data["mark"])
            play_instance = self.get_object()
            user_instance = request.user

            rating_instance, _ = Rating.objects.update_or_create(
                user=user_instance,
                play=play_instance,
                defaults={"mark": mark}
            )

            rating_instance.mark = mark
            rating_instance.save()

            return Response(
                {"message": "Rating set successfully."},
                status=status.HTTP_200_OK
            )
        except (ValueError, TypeError):
            return Response(
                {"error": "Invalid 'mark' in the request data."},
                status=status.HTTP_400_BAD_REQUEST
            )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="genres",
                type={"type": "array", "items": {"type": "number"}},
                description="A list of genre IDs",
                required=False,
            ),
            OpenApiParameter(
                name="actors",
                type={"type": "array", "items": {"type": "number"}},
                description="A list of actor IDs",
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_queryset(self):
        queryset = Genre.objects.all()

        # filtering by name
        name = self.request.query_params.get("name")

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                type={"type": "string"},
                description="Filter genres by name.",
                required=False,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ActorViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

    def get_serializer_class(self):
        if self.action == "upload_image":
            return ActorFotoSerializer

        if self.action == "list":
            return ActorListSerializer

        if self.action == "retrieve":
            return ActorDetailSerializer

        return ActorSerializer

    def get_queryset(self):
        queryset = Actor.objects.all()

        # filtering by full_name
        full_name = self.request.query_params.get("full_name")

        if full_name:
            queryset = queryset.filter(
                Q(
                    first_name__icontains=full_name) | Q(
                    last_name__icontains=full_name)
            )

        return queryset

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
        permission_classes=[IsAdminUser],
    )
    def upload_image(self, request, pk=None):
        item = self.get_object()
        serializer = self.get_serializer(item, data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="full_name",
                type={"type": "string"},
                description="Filter actors by full name.",
                required=False,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TheatreHallViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer

    def get_queryset(self):
        queryset = TheatreHall.objects.all()

        # filtering by name
        name = self.request.query_params.get("name")

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="name",
                type={"type": "string"},
                description="Filter theatre halls by name.",
                required=False,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PerformanceViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer

    def get_queryset(self):
        queryset = Performance.objects.all()

        # filtering by data
        date_param = self.request.query_params.get("date")

        if date_param:
            try:
                performance_date = date.fromisoformat(date_param)
                queryset = queryset.filter(show_time__date=performance_date)
            except ValueError:
                raise ParseError(
                    "Incorrect date format. Use the format 'YYYY-MM-DD'."
                )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer

        if self.action == "retrieve":
            return PerformanceDetailSerializer

        return PerformanceSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="date",
                type={"type": "string", "format": "date"},
                description=(
                        "Filter performances by date (format: YYYY-MM-DD)."
                ),
                required=False,
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    permission_classes = (IsAuthenticated,)

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
