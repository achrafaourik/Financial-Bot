"""
Tests for models.
"""
from django.contrib.auth import get_user_model
from decimal import Decimal
from django.test import TestCase
from core import models


class ModelsTests(TestCase):
    """Tests for the models"""

    def test_create_user_successful(self):
        """Tests that creating a user works properly"""
        email = "test@example.com"
        password = "password123"

        user = get_user_model().objects.create_user(
            email=email, password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test that email is normalized for new users"""
        sample_emails = [
            ["sample3@Example.com", "sample3@example.com"],
            ["sample2@EXAMPLE.com", "sample2@example.com"],
            ["sample1@EXAMPLE.COM", "sample1@example.com"],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email, password="pass123")
            self.assertEqual(user.email, expected)

    def test_user_creation_requires_email(self):
        """Test that creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", password="password123")

    def test_create_superuser(self):
        """Test that create_superuser works correctly"""
        user = get_user_model().objects.create_superuser(
            "sample@example.com", "123456")

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
