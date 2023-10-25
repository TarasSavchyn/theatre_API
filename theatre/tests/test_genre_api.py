from user.models import User

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from theatre.models import Genre
from theatre.serializers import GenreSerializer

GENRE_URL = reverse(
    "theatre:genre-list"
)  # Replace 'genre-list' with the actual URL name for listing genres.
GENRE_DETAIL_URL = reverse(
    "theatre:genre-detail", args=[1]
)  # Replace 'genre-detail' with the actual URL name for retrieving genre details.


class GenreAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_list_genres(self):
        """Test listing all genres."""
        response = self.client.get(GENRE_URL)

        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_retrieve_genre_details(self):
        """Test retrieving details of a single genre."""
        genre = Genre.objects.create(
            name="Drama",
        )
        response = self.client.get(GENRE_DETAIL_URL)

        serializer = GenreSerializer(genre)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class GenreAccessTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="test@test.ua", password="test123")
        self.genre = Genre.objects.create(name="Drama")

    def test_unauthenticated_user_cannot_access_genre_list_details(self):
        response = self.client.get(reverse("theatre:genre-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(
            reverse("theatre:genre-detail", args=[self.genre.id])
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_access_genre_list_details(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("theatre:genre-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(
            reverse("theatre:genre-detail", args=[self.genre.id])
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GenreModelTest(TestCase):
    def setUp(self):
        # Create a test Genre object
        Genre.objects.create(name="test")

    def test_name_unique(self):
        # Try to create a Genre with a name that already exists in the database
        duplicate_genre = Genre(name="test")
        # Ensure that an Exception is raised when attempting to save the duplicate
        with self.assertRaises(Exception):
            duplicate_genre.save()

    def test_str_representation(self):
        # Retrieve a Genre object from the database
        genre = Genre.objects.get(id=1)
        # Check if the string representation of the Genre is its name
        self.assertEqual(str(genre), genre.name)

    def test_read_genre(self):
        # Retrieve an existing Genre object
        genre = Genre.objects.get(name="test")
        # Ensure that the name of the retrieved Genre matches 'test'
        self.assertEqual(genre.name, "test")

    def test_update_genre(self):
        # Retrieve a Genre with the name 'test'
        genre = Genre.objects.get(name="test")
        # Update the name of the Genre
        genre.name = "TEST"
        genre.save()
        # Retrieve the updated Genre
        updated_genre = Genre.objects.get(id=genre.id)
        # Check if the name has been successfully updated to 'TEST'
        self.assertEqual(updated_genre.name, "TEST")

    def test_delete_genre(self):
        # Retrieve a Genre with the name 'test'
        genre = Genre.objects.get(name="test")
        # Delete the Genre
        genre.delete()
        # Attempt to retrieve the deleted Genre (should raise Genre.DoesNotExist)
        with self.assertRaises(Genre.DoesNotExist):
            Genre.objects.get(name="test")
