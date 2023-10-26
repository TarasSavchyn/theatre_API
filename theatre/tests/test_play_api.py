from theatre.serializers import PlayListSerializer, PlaySerializer
from user.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from theatre.models import Play, Genre, Actor

PLAY_URL = reverse("theatre:play-list")
PLAY_DETAIL_URL = reverse("theatre:play-detail", args=[1])


class PlayFilterTests(TestCase):
    """
    Test filtering plays by genre and actor.
    """

    def setUp(self):
        self.client = APIClient()
        self.genre1 = Genre.objects.create(name="Action")
        self.genre2 = Genre.objects.create(name="Drama")
        self.actor1 = Actor.objects.create(first_name="John", last_name="Doe")
        self.actor2 = Actor.objects.create(first_name="Jane", last_name="Smith")
        self.play1 = Play.objects.create(
            title="Play 1",
            description="Description 1",
        )
        self.play1.genres.add(self.genre1)
        self.play1.actors.add(self.actor1)
        self.play2 = Play.objects.create(
            title="Play 2",
            description="Description 2",
        )
        self.play2.genres.add(self.genre2)
        self.play2.actors.add(self.actor2)
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com", password="testpassword"
        )
        self.client.force_authenticate(user=self.user)

    def test_filter_plays_by_genre(self):
        """
        Test filtering plays by genre.
        """
        url = f"{PLAY_URL}?genres={self.genre1.id}"
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer1 = PlayListSerializer(self.play1)
        serializer2 = PlayListSerializer(self.play2)
        self.assertEqual(serializer1.data, res.data["results"][0])
        self.assertNotIn(serializer2.data, res.data["results"])

    def test_filter_plays_by_actor(self):
        """
        Test filtering plays by actor.
        """
        url = f"{PLAY_URL}?actors={self.actor1.id}"
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer1 = PlayListSerializer(self.play1)
        serializer2 = PlayListSerializer(self.play2)
        self.assertEqual(serializer1.data, res.data["results"][0])
        self.assertNotIn(serializer2.data, res.data["results"])


class PlayAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="testpassword"
        )
        self.client.force_authenticate(self.user)
        self.genre = Genre.objects.create(name="Test Genre")
        self.actor = Actor.objects.create(first_name="Test", last_name="Actor")
        self.play = Play.objects.create(
            title="Test Play", description="This is a test play"
        )
        self.play.genres.add(self.genre)
        self.play.actors.add(self.actor)

    def test_list_plays(self):
        """
        Test listing plays.
        """
        response = self.client.get(PLAY_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_play_details(self):
        """
        Test retrieving play details.
        """
        response = self.client.get(PLAY_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.play.title)
        self.assertEqual(response.data["description"], self.play.description)
        self.assertEqual(response.data["genres"][0]["name"], self.genre.name)
        self.assertEqual(response.data["actors"][0]["full_name"], self.actor.full_name)


class PlayAccessTestCase(TestCase):
    """
    Test access to play-related endpoints.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="test@test.ua", password="test123")
        self.play = Play.objects.create(
            title="Test Play", description="Description of the test play"
        )

    def test_unauthenticated_user_cannot_access_play_list_details(self):
        """
        Test unauthenticated user's access to play list details.
        """
        response = self.client.get(PLAY_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(PLAY_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_access_play_list_details(self):
        """
        Test authenticated user's access to play list details.
        """
        self.client.force_authenticate(user=self.user)
        response = self.client.get(PLAY_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(PLAY_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PlayModelTest(TestCase):
    def setUp(self):
        genre = Genre.objects.create(name="Drama")
        actor = Actor.objects.create(first_name="John", last_name="Doe")
        Play.objects.create(
            title="Test Play",
            description="A test play",
        )
        play = Play.objects.get(id=1)
        play.genres.add(genre)
        play.actors.add(actor)

    def test_genres_relationship(self):
        """
        Test the genres relationship of the Play model.
        """
        play = Play.objects.get(id=1)
        associated_genres = play.genres.all()
        self.assertEqual(associated_genres[0].name, "Drama")

    def test_actors_relationship(self):
        """
        Test the actors relationship of the Play model.
        """
        play = Play.objects.get(id=1)
        associated_actors = play.actors.all()
        self.assertEqual(associated_actors[0].full_name, "John Doe")

    def test_str_representation(self):
        """
        Test the string representation of the Play model.
        """
        play = Play.objects.get(id=1)
        self.assertEqual(str(play), play.title)

    def test_update_play(self):
        """
        Test updating the Play model.
        """
        play = Play.objects.get(id=1)
        play.title = "Updated Play Title"
        play.description = "Updated play description."
        play.save()
        updated_play = Play.objects.get(id=play.id)
        self.assertEqual(updated_play.title, "Updated Play Title")
        self.assertEqual(updated_play.description, "Updated play description.")

    def test_read_play(self):
        """
        Test reading an existing Play object.
        """
        play = Play.objects.get(title="Test Play")
        self.assertEqual(play.title, "Test Play")
        self.assertEqual(play.description, "A test play")

    def test_delete_play(self):
        """
        Test deleting a Play object.
        """
        play = Play.objects.get(title="Test Play")
        play.delete()
        with self.assertRaises(Play.DoesNotExist):
            Play.objects.get(title="Test Play")
