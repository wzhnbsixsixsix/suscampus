from django.test import TestCase
from announcements.forms import AnnouncementForm

class AnnouncementFormTests(TestCase):
    def test_valid_form(self):
        """Test that the form is valid when given correct data"""
        form_data = {"title": "Test Announcement", "content": "This is a test announcement."}
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
