from django.test import TestCase
from theatre.models import Reservation, Ticket
from django.contrib.auth import get_user_model


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
