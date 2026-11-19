from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from .models import Post, Category

class BlogPlatformTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="writer", password="StrongPass123!")
        self.post = Post.objects.create(author=self.user, title="Hello Django", content="Blog body", status="published")

    def test_home_shows_published_post(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Hello Django")

    def test_owner_can_open_edit_page(self):
        self.client.login(username="writer", password="StrongPass123!")
        response = self.client.get(reverse("post_edit", args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_cannot_open_dashboard(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 302)
