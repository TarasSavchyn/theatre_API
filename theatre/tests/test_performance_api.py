from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from user.models import User
from theatre.models import Performance, Play, TheatreHall
from datetime import datetime

class PerformanceAccessTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@test.ua',
            password='test123'
        )
        self.theatre_hall = TheatreHall.objects.create(
            name='Test Hall',
            rows=10,
            seats_in_row=10
        )
        self.play = Play.objects.create(
            title='Test Play',
            description='Description of the test play'
        )
        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.theatre_hall,
            show_time=datetime.now()
        )

    def test_unauthenticated_user_cannot_access_performance_list_details(self):
        response = self.client.get("/api/theatre/performances/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(f"/api/theatre/performances/{self.performance.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_access_performance_list_details(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/theatre/performances/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f"/api/theatre/performances/{self.performance.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PerformanceModelTest(TestCase):
    def setUp(self):
        # Create test Play and TheatreHall objects
        play = Play.objects.create(title="Test Play", description="A test play")
        theatre_hall = TheatreHall.objects.create(
            name="Main Hall", rows=10, seats_in_row=12
        )

        # Create a test Performance object
        self.performance = Performance.objects.create(
            play=play, theatre_hall=theatre_hall, show_time=datetime.now()
        )

    def test_str_representation(self):
        # Check the __str__ representation of Performance
        expected_str = f"{self.performance.play.title} at {self.performance.theatre_hall.name}, {self.performance.show_time}"
        self.assertEqual(str(self.performance), expected_str)

    def test_available_tickets(self):
        # Calculate the total capacity of the TheatreHall
        total_capacity = (
            self.performance.theatre_hall.rows
            * self.performance.theatre_hall.seats_in_row
        )

        # Check the available_tickets property
        self.assertEqual(self.performance.available_tickets, total_capacity)

    def test_update_performance(self):
        # Retrieve a Performance object
        performance = Performance.objects.get(id=self.performance.id)

        # Create a new TheatreHall for the update
        new_theatre_hall = TheatreHall.objects.create(
            name="Updated Hall", rows=8, seats_in_row=14
        )

        # Update the Performance with the new TheatreHall
        performance.theatre_hall = new_theatre_hall
        performance.save()

        # Retrieve the updated Performance
        updated_performance = Performance.objects.get(id=performance.id)

        # Check if the TheatreHall has been successfully updated
        self.assertEqual(updated_performance.theatre_hall.name, "Updated Hall")

    def test_read_performance(self):
        # Retrieve an existing Performance object
        performance = Performance.objects.get(id=self.performance.id)
        # Ensure that the associated Play and TheatreHall match the expected values
        self.assertEqual(performance.play.title, "Test Play")
        self.assertEqual(performance.theatre_hall.name, "Main Hall")

    def test_delete_performance(self):
        # Delete the Performance
        self.performance.delete()
        # Attempt to retrieve the deleted Performance (should raise Performance.DoesNotExist)
        with self.assertRaises(Performance.DoesNotExist):
            Performance.objects.get(id=self.performance.id)
