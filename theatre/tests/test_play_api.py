from user.models import User


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from theatre.models import Play, Genre, Actor

PLAY_URL = reverse("theatre:play-list")
PLAY_DETAIL_URL = reverse("theatre:play-detail", args=[1])


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
        response = self.client.get(PLAY_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_retrieve_play_details(self):
        response = self.client.get(PLAY_DETAIL_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.play.title)
        self.assertEqual(response.data["description"], self.play.description)
        self.assertEqual(response.data["genres"][0]["name"], self.genre.name)
        self.assertEqual(response.data["actors"][0]["full_name"], self.actor.full_name)


class PlayAccessTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="test@test.ua", password="test123")
        self.play = Play.objects.create(
            title="Test Play", description="Description of the test play"
        )

    def test_unauthenticated_user_cannot_access_play_list_details(self):
        response = self.client.get(PLAY_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(PLAY_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_access_play_list_details(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(PLAY_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(PLAY_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PlayModelTest(TestCase):
    def setUp(self):
        # Create test Genre and Actor objects
        genre = Genre.objects.create(name="Drama")
        actor = Actor.objects.create(first_name="John", last_name="Doe")

        # Create a test Play object
        Play.objects.create(
            title="Test Play",
            description="A test play",
        )

        # Add the test Genre and Actor to the Play
        play = Play.objects.get(id=1)
        play.genres.add(genre)
        play.actors.add(actor)

    def test_genres_relationship(self):
        # Retrieve a Play object
        play = Play.objects.get(id=1)
        # Retrieve the associated genres
        associated_genres = play.genres.all()
        # Check if the associated genres match the expected genre name
        self.assertEqual(associated_genres[0].name, "Drama")

    def test_actors_relationship(self):
        # Retrieve a Play object
        play = Play.objects.get(id=1)
        # Retrieve the associated actors
        associated_actors = play.actors.all()
        # Check if the associated actors match the expected actor full name
        self.assertEqual(associated_actors[0].full_name, "John Doe")

    def test_str_representation(self):
        # Retrieve a Play object
        play = Play.objects.get(id=1)
        # Check if the string representation of the Play is its title
        self.assertEqual(str(play), play.title)

    def test_update_play(self):
        # Retrieve a Play object
        play = Play.objects.get(id=1)
        # Update the title and description of the Play
        play.title = "Updated Play Title"
        play.description = "Updated play description."
        play.save()
        # Retrieve the updated Play
        updated_play = Play.objects.get(id=play.id)
        # Check if the title and description have been successfully updated
        self.assertEqual(updated_play.title, "Updated Play Title")
        self.assertEqual(updated_play.description, "Updated play description.")

    def test_read_play(self):
        # Retrieve an existing Play object
        play = Play.objects.get(title="Test Play")
        # Ensure that the title and description of the retrieved play match the expected values
        self.assertEqual(play.title, "Test Play")
        self.assertEqual(play.description, "A test play")

    def test_delete_play(self):
        # Retrieve a Play object
        play = Play.objects.get(title="Test Play")
        # Delete the Play
        play.delete()
        # Attempt to retrieve the deleted Play (should raise Play.DoesNotExist)
        with self.assertRaises(Play.DoesNotExist):
            Play.objects.get(title="Test Play")
