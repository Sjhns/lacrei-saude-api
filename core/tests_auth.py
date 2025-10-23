from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status


class JWTAuthTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.token_url = reverse("token_obtain_pair")
        self.professionals_url = reverse("professional-list")

    def test_obtain_token(self):
        data = {"username": "testuser", "password": "testpass"}
        r = self.client.post(self.token_url, data, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertIn("access", r.data)

    def test_access_protected_route_without_token(self):
        r = self.client.post(
            self.professionals_url,
            {"name_social": "Alex", "profession": "Médico"},
            format="json",
        )
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_protected_route_with_token(self):
        token_response = self.client.post(
            self.token_url,
            {"username": "testuser", "password": "testpass"},
            format="json",
        )
        token = token_response.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        r = self.client.post(
            self.professionals_url,
            {"name_social": "Alex", "profession": "Médico"},
            format="json",
        )
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
