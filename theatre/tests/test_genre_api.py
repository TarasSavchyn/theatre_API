from django.test import TestCase
from theatre.models import Genre


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
