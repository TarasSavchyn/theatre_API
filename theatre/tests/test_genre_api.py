from user.models import User
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from theatre.models import Genre
from theatre.serializers import GenreSerializer

GENRE_URL = reverse("theatre:genre-list")
GENRE_DETAIL_URL = reverse("theatre:genre-detail", args=[1])


class GenreFilterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

        self.genre1 = Genre.objects.create(name="Action")
        self.genre2 = Genre.objects.create(name="Drama")
        self.genre3 = Genre.objects.create(name="Comedy")

    def test_filter_genres_by_name(self):
        """
        Test filtering genres by name.
        """
        url = f"{GENRE_URL}?name=Action"
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer1 = GenreSerializer(self.genre1)
        serializer2 = GenreSerializer(self.genre2)
        serializer3 = GenreSerializer(self.genre3)
        self.assertEqual(serializer1.data, res.data["results"][0])
        self.assertNotIn(serializer2.data, res.data["results"])
        self.assertNotIn(serializer3.data, res.data["results"])


class GenreAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_list_genres(self):
        """
        Test listing all genres.
        """
        response = self.client.get(GENRE_URL)

        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_retrieve_genre_details(self):
        """
        Test retrieving details of a single genre.
        """
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
        """
        Test that an unauthenticated user cannot access the list of genres and genre details.
        """
        response = self.client.get(reverse("theatre:genre-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(GENRE_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_access_genre_list_details(self):
        """
        Test that an authenticated user can access the list of genres and genre details.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("theatre:genre-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(GENRE_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GenreModelTest(TestCase):
    def setUp(self):
        # Create a test Genre object
        Genre.objects.create(name="test")

    def test_name_unique(self):
        """
        Test that genre names are unique and cannot be duplicated.
        """
        # Try to create a Genre with a name that already exists in the database
        duplicate_genre = Genre(name="test")
        # Ensure that an Exception is raised when attempting to save the duplicate
        with self.assertRaises(Exception):
            duplicate_genre.save()

    def test_str_representation(self):
        """
        Test the string representation of the Genre model.
        """
        genre = Genre.objects.get(id=1)
        self.assertEqual(str(genre), genre.name)

    def test_read_genre(self):
        """
        Test reading an existing Genre object.
        """
        genre = Genre.objects.get(name="test")
        self.assertEqual(genre.name, "test")

    def test_update_genre(self):
        """
        Test updating an existing Genre's name.
        """
        genre = Genre.objects.get(name="test")
        genre.name = "TEST"
        genre.save()
        updated_genre = Genre.objects.get(id=genre.id)
        self.assertEqual(updated_genre.name, "TEST")

    def test_delete_genre(self):
        """
        Test deleting a Genre object.
        """
        genre = Genre.objects.get(name="test")
        genre.delete()
        with self.assertRaises(Genre.DoesNotExist):
            Genre.objects.get(name="test")
