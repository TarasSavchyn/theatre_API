from django.test import TestCase
from user.models import User
from theatre.models import Rating, Play


class RatingCRUDTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@test.ua", password="test123")
        self.admin = User.objects.create_user(email="admin@test.ua", password="test123")
        self.play = Play.objects.create(
            title="Test Play", description="Description of the test play"
        )
        self.rating = Rating.objects.create(play=self.play, mark=4.5, user=self.user)

    def test_read_rating(self):
        """
        Test reading a Rating object.
        """
        retrieved_rating = Rating.objects.get(id=self.rating.id)
        self.assertEqual(retrieved_rating.play, self.play)
        self.assertEqual(retrieved_rating.mark, 4.5)
        self.assertEqual(retrieved_rating.user, self.user)

    def test_update_rating(self):
        """
        Test updating a Rating object.
        """
        self.rating.mark = 3.0
        self.rating.save()
        updated_rating = Rating.objects.get(id=self.rating.id)
        self.assertEqual(updated_rating.mark, 3.0)

    def test_delete_rating(self):
        """
        Test deleting a Rating object.
        """
        rating_id = self.rating.id
        self.rating.delete()
        with self.assertRaises(Rating.DoesNotExist):
            Rating.objects.get(id=rating_id)

    def test_create_rating(self):
        """
        Test creating a new Rating object.
        """
        new_rating = Rating.objects.create(play=self.play, mark=3.0, user=self.admin)
        self.assertEqual(new_rating.play, self.play)
        self.assertEqual(new_rating.mark, 3.0)
        self.assertEqual(new_rating.user, self.admin)
