from django.test import TestCase
from django.contrib.auth import get_user_model
from announcements.models import Announcement

User = get_user_model()  # Use CustomUser model from accounts

class AnnouncementModelTests(TestCase):
    def setUp(self):
        """Set up test data for users and announcements"""
        self.user = User.objects.create_user(username="testuser", password="password", role="game_keeper") # creating an example user
        self.announcement = Announcement.objects.create(
            title="Test Announcement",
            content="This is a test announcement.",
            author=self.user
        )

    def test_announcement_creation(self):
        """Test that an announcement is created correctly"""
        self.assertEqual(self.announcement.title, "Test Announcement") # makes sure the post matches the users post
        self.assertEqual(self.announcement.content, "This is a test announcement.")
        self.assertEqual(self.announcement.author, self.user)
        self.assertTrue(self.announcement.created_at)  # Ensure timestamp is auto-generated

    def test_announcement_str(self):
        """Test the __str__ method of Announcement"""
        self.assertEqual(str(self.announcement), "Test Announcement")

    def test_get_author_role(self):
        """Test get_author_role method"""
        self.assertEqual(self.announcement.get_author_role(), "game_keeper")  # Role should match the user
