from theatre.serializers import PerformanceListSerializer
from user.models import User
from theatre.models import Play, TheatreHall
from datetime import datetime

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from theatre.models import Performance

PERFORMANCE_URL = reverse("theatre:performance-list")
PERFORMANCE_DETAIL_URL = reverse("theatre:performance-detail", args=[1])


class PerformanceFilterTests(TestCase):
    def setUp(self):
        """
        Set up the test environment and create sample data for performance filtering tests.
        """
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

        self.theatre_hall = TheatreHall.objects.create(
            name="Main Hall", rows=10, seats_in_row=15
        )
        self.play1 = Play.objects.create(title="Play 1", description="Description 1")
        self.play2 = Play.objects.create(title="Play 2", description="Description 2")

        self.performance1 = Performance.objects.create(
            play=self.play1,
            theatre_hall=self.theatre_hall,
            show_time=datetime(2023, 10, 28),
        )
        self.performance2 = Performance.objects.create(
            play=self.play1,
            theatre_hall=self.theatre_hall,
            show_time=datetime(2023, 10, 30),
        )
        self.performance3 = Performance.objects.create(
            play=self.play2,
            theatre_hall=self.theatre_hall,
            show_time=datetime(2023, 11, 1),
        )

    def test_filter_performances_by_date(self):
        """
        Test filtering performances by date.
        """
        url = f"{PERFORMANCE_URL}?date=2023-10-30"
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer1 = PerformanceListSerializer(self.performance2)
        serializer2 = PerformanceListSerializer(self.performance1)
        serializer3 = PerformanceListSerializer(self.performance3)
        self.assertIn(serializer1.data, res.data["results"])
        self.assertNotIn(serializer2.data, res.data["results"])
        self.assertNotIn(serializer3.data, res.data["results"])


class PerformanceAPITests(TestCase):
    def setUp(self):
        """
        Set up the test environment and create sample data for performance API tests.
        """
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="testpassword"
        )
        self.client.force_authenticate(self.user)

        self.theatre_hall = TheatreHall.objects.create(
            name="Test Hall", rows=10, seats_in_row=15
        )
        self.play = Play.objects.create(
            title="Test Play", description="This is a test play"
        )
        self.performance = Performance.objects.create(
            play=self.play, theatre_hall=self.theatre_hall, show_time="2023-10-20"
        )

    def test_list_performances(self):
        """
        Test listing all performances.
        """
        response = self.client.get(PERFORMANCE_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_performance_details(self):
        """
        Test retrieving details of a single performance.
        """
        response = self.client.get(PERFORMANCE_DETAIL_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["play"]["title"], self.play.title)
        self.assertEqual(response.data["theatre_hall"]["name"], self.theatre_hall.name)


class PerformanceAccessTestCase(TestCase):
    def setUp(self):
        """
        Set up the test environment and create sample data for performance access tests.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(email="test@test.ua", password="test123")
        self.theatre_hall = TheatreHall.objects.create(
            name="Test Hall", rows=10, seats_in_row=10
        )
        self.play = Play.objects.create(
            title="Test Play", description="Description of the test play"
        )
        self.performance = Performance.objects.create(
            play=self.play, theatre_hall=self.theatre_hall, show_time=datetime.now()
        )

    def test_unauthenticated_user_cannot_access_performance_list_details(self):
        """
        Test that unauthenticated users cannot access performance list and details.
        """
        response = self.client.get(reverse("theatre:performance-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(
            reverse("theatre:performance-detail", args=[self.performance.id])
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_access_performance_list_details(self):
        """
        Test that authenticated users can access performance list and details.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("theatre:performance-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(
            reverse("theatre:performance-detail", args=[self.performance.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PerformanceModelTest(TestCase):
    def setUp(self):
        """
        Set up the test environment and create a test performance object.
        """
        play = Play.objects.create(title="Test Play", description="A test play")
        theatre_hall = TheatreHall.objects.create(
            name="Main Hall", rows=10, seats_in_row=12
        )

        self.performance = Performance.objects.create(
            play=play, theatre_hall=theatre_hall, show_time=datetime.now()
        )

    def test_str_representation(self):
        """
        Test the string representation of a performance.
        """
        expected_str = f"{self.performance.play.title} at {self.performance.theatre_hall.name}, {self.performance.show_time}"
        self.assertEqual(str(self.performance), expected_str)

    def test_available_tickets(self):
        """
        Test the available_tickets property of a performance.
        """
        total_capacity = (
            self.performance.theatre_hall.rows
            * self.performance.theatre_hall.seats_in_row
        )

        self.assertEqual(self.performance.available_tickets, total_capacity)

    def test_update_performance(self):
        """
        Test updating a performance's theatre hall.
        """
        performance = Performance.objects.get(id=self.performance.id)

        new_theatre_hall = TheatreHall.objects.create(
            name="Updated Hall", rows=8, seats_in_row=14
        )

        performance.theatre_hall = new_theatre_hall
        performance.save()

        updated_performance = Performance.objects.get(id=performance.id)

        self.assertEqual(updated_performance.theatre_hall.name, "Updated Hall")

    def test_read_performance(self):
        """
        Test reading a performance and its associated play and theatre hall.
        """
        performance = Performance.objects.get(id=self.performance.id)
        self.assertEqual(performance.play.title, "Test Play")
        self.assertEqual(performance.theatre_hall.name, "Main Hall")

    def test_delete_performance(self):
        """
        Test deleting a performance.
        """
        self.performance.delete()
        with self.assertRaises(Performance.DoesNotExist):
            Performance.objects.get(id=self.performance.id)
