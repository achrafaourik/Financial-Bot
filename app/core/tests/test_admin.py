"""
Tests for the django admin interface modifications.
"""
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client


class AdminSiteTest(TestCase):
    """Tests for Django admin"""

    def setUp(self):
        """Create a user and client"""
        self.client = Client()

        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com", password="password"
        )

        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="password", name="Test User"
        )

    def test_list_users(self):
        """Test that the admin page lists users"""
        url = reverse("admin:core_user_changelist")
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.admin_user.email)

    def test_user_edit_page(self):
        """Test that the user edit page works properly"""
        url = reverse("admin:core_user_change", args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the user create page works properly"""
        url = reverse("admin:core_user_add")
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
