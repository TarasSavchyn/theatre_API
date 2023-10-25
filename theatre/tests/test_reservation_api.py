from django.test import TestCase
from django.urls import reverse

from theatre.models import Reservation, TheatreHall, Performance, Play
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from user.models import User
from rest_framework.test import APITestCase
from rest_framework import status


RESERVATION_URL = reverse("theatre:reservation-list")


class ReservationAPITests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
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
        self.reservation_data = {
            "user": self.user.id,
            "status": True,
            "tickets": [{"row": 1, "seat": 2, "performance": self.performance.id}],
        }

    def test_create_reservation(self):
        response = self.client.post(
            RESERVATION_URL, self.reservation_data, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 1)
        reservation = Reservation.objects.first()
        self.assertEqual(reservation.status, True)
        self.assertEqual(reservation.user, self.user)
        self.assertEqual(reservation.tickets.count(), 1)

    def test_retrieve_reservation(self):
        response = self.client.get(RESERVATION_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cancel_reservation(self):
        response = self.client.post(
            RESERVATION_URL, self.reservation_data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reservation_id = response.data.get("id")

        response = self.client.post(
            f"{RESERVATION_URL}{reservation_id}/cancel/", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        reservation = Reservation.objects.get(id=reservation_id)
        self.assertFalse(reservation.status)


class ReservationAccessTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(email="user1@test.ua", password="test123")
        self.user2 = User.objects.create_user(email="user2@test.ua", password="test123")
        self.reservation_user1 = Reservation.objects.create(
            user=self.user1, status=True
        )

        self.reservation_user2 = Reservation.objects.create(
            user=self.user2, status=True
        )
        self.url = "/api/theatre/reservations/"

    def test_unauthenticated_user_cannot_access_reservations(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_access_own_reservations(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_authenticated_user_cannot_access_other_user_reservations(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.get(
            f"/api/theatre/reservations/{self.reservation_user2.id}/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_user_can_cancel_own_reservation(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(
            f"/api/theatre/reservations/{self.reservation_user1.id}/cancel/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.reservation_user1.refresh_from_db()
        self.assertFalse(self.reservation_user1.status)

    def test_authenticated_user_cannot_cancel_other_user_reservation(self):
        self.client.force_authenticate(user=self.user1)
        response = self.client.post(
            f"/api/theatre/reservations/{self.reservation_user2.id}/cancel/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.reservation_user2.refresh_from_db()
        self.assertTrue(self.reservation_user2.status)


class ReservationModelTest(TestCase):
    def setUp(self):
        # Create a test User
        self.user = get_user_model().objects.create_user("test@test.ua", "test123")
        # Create a test Reservation with the User
        self.reservation = Reservation.objects.create(user=self.user)

    def test_update_reservation(self):
        # Update the status of the Reservation
        self.reservation.status = False
        self.reservation.save()
        # Retrieve the updated Reservation
        updated_reservation = Reservation.objects.get(id=self.reservation.id)
        # Check if the status has been successfully updated
        self.assertFalse(updated_reservation.status)

    def test_read_reservation(self):
        # Retrieve an existing Reservation object
        reservation = Reservation.objects.get(id=self.reservation.id)
        # Ensure that the associated User matches the expected value
        self.assertEqual(reservation.user.email, "test@test.ua")

    def test_delete_reservation(self):
        # Delete the Reservation
        self.reservation.delete()
        # Attempt to retrieve the deleted Reservation (should raise Reservation.DoesNotExist)
        with self.assertRaises(Reservation.DoesNotExist):
            Reservation.objects.get(id=self.reservation.id)

    def test_str_representation(self):
        # Check if the string representation of the Reservation
        expected_str = f"Reservation by {self.user.first_name} {self.user.last_name}"
        self.assertEqual(str(self.reservation), expected_str)
