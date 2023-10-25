from user.models import User


import tempfile
import os
from PIL import Image

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from theatre.models import Actor
from theatre.serializers import ActorListSerializer, ActorDetailSerializer

ACTOR_URL = reverse("theatre:actor-list")
ACTOR_DETAIL_URL = reverse("theatre:actor-detail", args=[1])


def image_upload_url(actor_id):
    return reverse("theatre:actor-upload-image", args=[actor_id])


class ActorAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_list_actors(self):
        """Test listing all actors."""
        response = self.client.get(ACTOR_URL)

        actors = Actor.objects.all()
        serializer = ActorListSerializer(actors, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_retrieve_actor_details(self):
        """Test retrieving details of a single actor."""
        actor = Actor.objects.create(
            first_name="John",
            last_name="Doe",
        )
        response = self.client.get(ACTOR_DETAIL_URL)

        serializer = ActorDetailSerializer(actor)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)


class ActorImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.actor = Actor.objects.create(first_name="John", last_name="Doe")

    def tearDown(self):
        self.actor.foto.delete()

    def test_upload_image_to_actor(self):
        url = image_upload_url(self.actor.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(url, {"foto": ntf}, format="multipart")
        self.actor.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("foto", res.data)
        self.assertTrue(os.path.exists(self.actor.foto.path))

    #
    def test_upload_image_bad_request(self):
        url = image_upload_url(self.actor.id)
        res = self.client.post(url, {"foto": "not image"}, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_image_url_is_shown_on_actor(self):
        url = image_upload_url(self.actor.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"foto": ntf}, format="multipart")

        res = self.client.get(ACTOR_DETAIL_URL)
        self.assertIn("foto", res.data)

        res = self.client.get(ACTOR_URL)
        self.assertIn("foto", res.data["results"][0])


class ActorAccessTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="test@test.ua", password="test123")
        self.actor = Actor.objects.create(first_name="John", last_name="Doe")

    def test_unauthenticated_user_cannot_access_actor_list_details(self):
        response = self.client.get(reverse("theatre:actor-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(ACTOR_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_access_actor_list_details(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("theatre:actor-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(ACTOR_DETAIL_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ActorModelTest(TestCase):
    def setUp(self):
        # Create a test Actor object
        self.actor = Actor.objects.create(first_name="John", last_name="Doe")

    def test_full_name_property(self):
        # Retrieve an Actor object
        actor = Actor.objects.get(id=self.actor.id)
        # Check if the `full_name` property returns the expected full name
        expected_full_name = "John Doe"
        self.assertEqual(actor.full_name, expected_full_name)

    def test_read_actor(self):
        # Retrieve an existing Actor object
        actor = Actor.objects.get(id=self.actor.id)
        # Ensure that the first name and last name of the retrieved actor match the expected values
        self.assertEqual(actor.first_name, "John")
        self.assertEqual(actor.last_name, "Doe")

    def test_update_actor(self):
        # Retrieve an Actor with the first name 'John'
        actor = Actor.objects.get(first_name="John")
        # Update the first name and last name of the actor
        actor.first_name = "Jane"
        actor.last_name = "Smith"
        actor.save()
        # Retrieve the updated Actor
        updated_actor = Actor.objects.get(id=actor.id)
        # Check if the first name and last name have been successfully updated
        self.assertEqual(updated_actor.first_name, "Jane")
        self.assertEqual(updated_actor.last_name, "Smith")

    def test_delete_actor(self):
        # Retrieve an Actor with the first name 'John'
        actor = Actor.objects.get(id=self.actor.id)
        # Delete the Actor
        actor.delete()
        # Attempt to retrieve the deleted Actor (should raise Actor.DoesNotExist)
        with self.assertRaises(Actor.DoesNotExist):
            Actor.objects.get(id=self.actor.id)

    def test_str_representation(self):
        # Check the __str__ representation of Actor
        expected_str = f"{self.actor.first_name} {self.actor.last_name}"
        self.assertEqual(str(self.actor), expected_str)
