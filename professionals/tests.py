from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Professional
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class ProfessionalCRUDTest(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(username="tester", password="123456")
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        self.list_url = reverse("professional-list")
        self.obj = Professional.objects.create(
            name_social="Alex", profession="Psicólogo"
        )

    def test_list_professionals(self):
        r = self.client.get(self.list_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(r.data), 1)

    def test_create_professional(self):
        payload = {"name_social": "Jo", "profession": "Médico"}
        r = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Professional.objects.count(), 2)

    def test_update_professional(self):
        url = reverse("professional-detail", args=[self.obj.id])
        r = self.client.patch(url, {"profession": "Enfermeiro"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.obj.refresh_from_db()
        self.assertEqual(self.obj.profession, "Enfermeiro")

    def test_delete_professional(self):
        url = reverse("professional-detail", args=[self.obj.id])
        r = self.client.delete(url)
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Professional.objects.filter(id=self.obj.id).exists())

    def test_unauthorized_access(self):
        """Verifica se a API retorna 401 sem autenticação"""
        self.client.credentials()  # remove o token
        r = self.client.get(self.list_url)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)
