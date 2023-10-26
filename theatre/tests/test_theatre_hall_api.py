from theatre.serializers import TheatreHallSerializer
from user.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from theatre.models import TheatreHall

THEATREHALL_URL = reverse("theatre:theatrehall-list")
THEATREHALL_DETAIL_URL = reverse("theatre:theatrehall-detail", args=[1])


class TheatreHallFilterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

        self.hall1 = TheatreHall.objects.create(name="Hall 1", rows=2, seats_in_row=2)
        self.hall2 = TheatreHall.objects.create(name="Hall 2", rows=2, seats_in_row=2)
        self.hall3 = TheatreHall.objects.create(
            name="Small Hall", rows=2, seats_in_row=2
        )

    def test_filter_halls_by_name(self):
        """
        Test filtering theatre halls by name.
        """
        url = f"{THEATREHALL_URL}?name=Hall 1"
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer1 = TheatreHallSerializer(self.hall1)
        serializer2 = TheatreHallSerializer(self.hall2)
        serializer3 = TheatreHallSerializer(self.hall3)
        self.assertEqual(serializer1.data, res.data["results"][0])
        self.assertNotIn(serializer2.data, res.data["results"])
        self.assertNotIn(serializer3.data, res.data["results"])


class TheatreHallAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="testpassword"
        )
        self.client.force_authenticate(self.user)

        self.theatre_hall = TheatreHall.objects.create(
            name="Test Hall", rows=10, seats_in_row=15
        )

    def test_list_theatrehalls(self):
        """
        Test getting a list of theatre halls.
        """
        response = self.client.get(THEATREHALL_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_theatrehall_details(self):
        """
        Test retrieving details of a theatre hall.
        """
        response = self.client.get(THEATREHALL_DETAIL_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.theatre_hall.name)
        self.assertEqual(response.data["rows"], self.theatre_hall.rows)
        self.assertEqual(response.data["seats_in_row"], self.theatre_hall.seats_in_row)
        self.assertEqual(response.data["seats_in_row"], self.theatre_hall.seats_in_row)


class TheatreHallAccessTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="test@test.ua", password="test123")
        self.theatre_hall = TheatreHall.objects.create(
            name="Test Hall", rows=10, seats_in_row=10
        )

    def test_unauthenticated_user_cannot_access_theatrehall_list_details(self):
        """
        Test that unauthenticated users cannot access the list and details of theatre halls.
        """
        response = self.client.get(THEATREHALL_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(THEATREHALL_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_access_theatrehall_list_details(self):
        """
        Test that authenticated users can access the list and details of theatre halls.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(THEATREHALL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(THEATREHALL_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TheatreHallModelTest(TestCase):
    def setUp(self):
        """
        Set up a test TheatreHall object.
        """
        TheatreHall.objects.create(name="Test Hall", rows=10, seats_in_row=15)

    def test_capacity_calculation(self):
        """
        Test the calculation of the capacity.
        """
        hall = TheatreHall.objects.get(id=1)
        expected_capacity = hall.rows * hall.seats_in_row
        self.assertEqual(hall.capacity, expected_capacity)

    def test_read_theatre_hall(self):
        """
        Test reading a Theatre Hall.
        """
        hall = TheatreHall.objects.get(name="Test Hall")
        self.assertEqual(hall.name, "Test Hall")
        self.assertEqual(hall.rows, 10)
        self.assertEqual(hall.seats_in_row, 15)

    def test_update_theatre_hall(self):
        """
        Test updating a Theatre Hall.
        """
        hall = TheatreHall.objects.get(name="Test Hall")
        hall.name = "Updated Hall"
        hall.seats_in_row = 20
        hall.save()
        updated_hall = TheatreHall.objects.get(id=hall.id)
        self.assertEqual(updated_hall.name, "Updated Hall")
        self.assertEqual(updated_hall.seats_in_row, 20)

    def test_delete_theatre_hall(self):
        """
        Test deleting a Theatre Hall.
        """
        hall = TheatreHall.objects.get(name="Test Hall")
        hall.delete()
        with self.assertRaises(TheatreHall.DoesNotExist):
            TheatreHall.objects.get(name="Test Hall")

    def test_str_representation(self):
        """
        Test the string representation of a TheatreHall object.
        """
        hall = TheatreHall.objects.get(name="Test Hall")
        expected_str = "Test Hall"
        self.assertEqual(str(hall), expected_str)
