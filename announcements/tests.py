from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from announcements.forms import AnnouncementForm
from announcements.models import Announcement
from accounts.models import CustomUser


# Create your tests here.

User = get_user_model()

class AnnouncementFormTests(TestCase):
    def test_valid_form(self):
        """Test that the form is valid when given correct data"""
        form_data = {"title": "Test Announcement", "summary":"test summary", "content": "This is a test announcement."}
        form = AnnouncementForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_missing_title(self):
        """Test that the form is invalid when title is missing"""
        form_data = {"title": "", "content": "This is a test announcement."}
        form = AnnouncementForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_missing_content(self):
        """Test that the form is invalid when content is missing"""
        form_data = {"title": "Test Announcement", "content": ""}
        form = AnnouncementForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("content", form.errors)

    def test_title_max_length(self):
        """Test that the title cannot exceed 200 characters"""
        long_title = "A" * 201  # 201 characters
        form_data = {"title": long_title, "content": "Valid content"}
        form = AnnouncementForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

class AnnouncementModelTests(TestCase):
    def setUp(self):
        """Set up test data for users and announcements"""
        self.user = CustomUser.objects.create_user(username="testuser", password="password", role="game_keeper") # creating an example user
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



class AnnouncementViewTests(TestCase):
    def setUp(self):
        """Set up test data for users and announcements"""
        self.client = Client()

        # Create users: a Game Keeper and a Player
        self.game_keeper = CustomUser.objects.create_user(username="gamekeeper", password="TestPassword12345", role="gameKeeper", verified=True)
        self.player = CustomUser.objects.create_user(username="player", password="TestPassword12345", role="player", verified=True)

        

        # Create a sample announcement
        self.announcement = Announcement.objects.create(
            title="Test Announcement",
            summary="test summary",
            content="This is a test announcement.",
            image=None,
            author=self.game_keeper
        )

    def test_announcement_list_view(self):
        """Ensure announcement list view is accessible"""
        self.client.login(username="player", password="TestPassword12345")
        response = self.client.get(reverse("announcement_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Announcement")

    def test_create_announcement_requires_login(self):
        """Ensure unauthenticated users are redirected to login page"""
        response = self.client.get(reverse("create_announcement"))
        self.assertRedirects(response, "/accounts/login/?next=/announcements/create/")

    def test_create_announcement_denies_players(self):
        """Ensure players (non-Game Keepers) cannot create announcements"""
        self.client.login(username="player", password="TestPassword12345")
        response = self.client.post(reverse("create_announcement"), {
            "title": "Unauthorized Announcement",
            "content": "This should not be allowed."
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/announcements/")  # Redirected with error message
        self.assertFalse(Announcement.objects.filter(title="Unauthorized Announcement").exists())

    def test_create_announcement_successful(self):
        """Ensure Game Keepers can create announcements"""
        self.client.login(username="gamekeeper", password="TestPassword12345")
        response = self.client.post(reverse("create_announcement"), {
            "title": "New Announcement",
            "summary":"test summary",
            "content": "This is a valid announcement."
        })
        self.assertRedirects(response, reverse("announcement_list"))
        self.assertTrue(Announcement.objects.filter(title="New Announcement").exists())
