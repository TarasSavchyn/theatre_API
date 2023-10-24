from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from theatre.models import Actor
from rest_framework.test import APIClient

from user.models import User


class ActorAccessTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email='test@test.ua',
            password='test123'
        )
        self.actor = Actor.objects.create(
            first_name='John',
            last_name='Doe'
        )

    def test_unauthenticated_user_cannot_access_actor_list_details(self):
        response = self.client.get("http://localhost/api/theatre/actors/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(f"/api/theatre/actors/{self.actor.id}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_access_actor_list_details(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get("http://localhost/api/theatre/actors/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(f"/api/theatre/actors/{self.actor.id}/")
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



