from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from announcements.models import Announcement

User = get_user_model()

class AnnouncementViewTests(TestCase):
    def setUp(self):
        """Set up test data for users and announcements"""
        self.client = Client()

        # Create users: a Game Keeper and a Player
        self.game_keeper = User.objects.create_user(username="gamekeeper", password="password", role="game_keeper")
        self.player = User.objects.create_user(username="player", password="password", role="player")

        # Create a sample announcement
        self.announcement = Announcement.objects.create(
            title="Test Announcement",
            content="This is a test announcement.",
            author=self.game_keeper
        )

    def test_announcement_list_view(self):
        """Ensure announcement list view is accessible"""
        response = self.client.get(reverse("announcement_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Announcement")

    def test_create_announcement_requires_login(self):
        """Ensure unauthenticated users are redirected to login page"""
        response = self.client.get(reverse("create_announcement"))
        self.assertRedirects(response, "/accounts/login/")

    def test_create_announcement_denies_players(self):
        """Ensure players (non-Game Keepers) cannot create announcements"""
        self.client.login(username="player", password="password")
        response = self.client.post(reverse("create_announcement"), {
            "title": "Unauthorized Announcement",
            "content": "This should not be allowed."
        })
        self.assertRedirects(response, "/announcements/")  # Redirected with error message
        self.assertFalse(Announcement.objects.filter(title="Unauthorized Announcement").exists())

    def test_create_announcement_successful(self):
        """Ensure Game Keepers can create announcements"""
        self.client.login(username="gamekeeper", password="password")
        response = self.client.post(reverse("create_announcement"), {
            "title": "New Announcement",
            "content": "This is a valid announcement."
        })
        self.assertRedirects(response, reverse("announcement_list"))
        self.assertTrue(Announcement.objects.filter(title="New Announcement").exists())
