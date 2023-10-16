from django.test import TestCase
from theatre.models import Actor


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
