from django.test import TestCase
from theatre.models import Play, Genre, Actor


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
