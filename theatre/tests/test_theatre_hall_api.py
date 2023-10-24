from django.test import TestCase
from theatre.models import TheatreHall

from rest_framework import status
from rest_framework.test import APIClient
from user.models import User

class TheatreHallAccessTestCase(TestCase):
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

    def test_unauthenticated_user_cannot_access_theatrehall_list_details(self):
        response = self.client.get("/api/theatre/theatrehalls/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(f"/api/theatre/theatrehalls/{self.theatre_hall.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_access_theatrehall_list_details(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/api/theatre/theatrehalls/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f"/api/theatre/theatrehalls/{self.theatre_hall.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TheatreHallModelTest(TestCase):
    def setUp(self):
        # Create a test TheatreHall object
        TheatreHall.objects.create(name="Test Hall", rows=10, seats_in_row=15)

    def test_capacity_calculation(self):
        # Retrieve a TheatreHall object
        hall = TheatreHall.objects.get(id=1)
        # Calculate the expected capacity based on rows and seats_in_row
        expected_capacity = hall.rows * hall.seats_in_row
        # Check if the calculated capacity matches the expected value
        self.assertEqual(hall.capacity, expected_capacity)

    def test_read_theatre_hall(self):
        # Retrieve an existing TheatreHall object
        hall = TheatreHall.objects.get(name="Test Hall")
        # Ensure that the name, rows, and seats_in_row of the retrieved hall match the expected values
        self.assertEqual(hall.name, "Test Hall")
        self.assertEqual(hall.rows, 10)
        self.assertEqual(hall.seats_in_row, 15)

    def test_update_theatre_hall(self):
        # Retrieve a TheatreHall with the name 'Test Hall'
        hall = TheatreHall.objects.get(name="Test Hall")
        # Update the name and seats_in_row of the hall
        hall.name = "Updated Hall"
        hall.seats_in_row = 20
        hall.save()
        # Retrieve the updated TheatreHall
        updated_hall = TheatreHall.objects.get(id=hall.id)
        # Check if the name and seats_in_row have been successfully updated
        self.assertEqual(updated_hall.name, "Updated Hall")
        self.assertEqual(updated_hall.seats_in_row, 20)

    def test_delete_theatre_hall(self):
        # Retrieve a TheatreHall with the name 'Test Hall'
        hall = TheatreHall.objects.get(name="Test Hall")
        # Delete the TheatreHall
        hall.delete()
        # Attempt to retrieve the deleted TheatreHall (should raise TheatreHall.DoesNotExist)
        with self.assertRaises(TheatreHall.DoesNotExist):
            TheatreHall.objects.get(name="Test Hall")

    def test_str_representation(self):
        # Retrieve a TheatreHall object
        hall = TheatreHall.objects.get(name="Test Hall")
        # Expect that the string representation (__str__) of the object would be 'Test Hall'
        expected_str = "Test Hall"
        self.assertEqual(str(hall), expected_str)
