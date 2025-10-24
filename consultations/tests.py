from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from professionals.models import Professional
from .models import Consultation
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class ConsultationCRUDTest(APITestCase):
    def setUp(self):

        self.user = User.objects.create_user(username="tester", password="123456")
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

        self.professional = Professional.objects.create(
            name_social="Alex", profession="Psicólogo"
        )

        self.list_url = reverse("consultation-list")
        self.valid_payload = {
            "datetime": (timezone.now() + timedelta(days=1)).isoformat(),
            "professional": self.professional.id,
            "notes": "Primeira consulta",
        }

    def test_list_consultations(self):
        Consultation.objects.create(
            professional=self.professional,
            datetime=timezone.now() + timedelta(days=1),
            notes="teste",
        )
        r = self.client.get(self.list_url)
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(r.data), 1)

    def test_create_consultation(self):
        r = self.client.post(self.list_url, self.valid_payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Consultation.objects.count(), 1)

    def test_create_with_nonexistent_professional(self):
        payload = self.valid_payload.copy()
        payload["professional"] = 9999  # profissional inexistente
        r = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_consultation(self):
        consultation = Consultation.objects.create(
            professional=self.professional,
            datetime=timezone.now() + timedelta(days=2),
            notes="Antiga",
        )
        url = reverse("consultation-detail", args=[consultation.id])
        new_time = (timezone.now() + timedelta(days=3)).isoformat()
        r = self.client.patch(
            url, {"datetime": new_time, "notes": "Atualizada"}, format="json"
        )
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        consultation.refresh_from_db()
        self.assertEqual(consultation.notes, "Atualizada")

    def test_delete_consultation(self):
        consultation = Consultation.objects.create(
            professional=self.professional,
            datetime=timezone.now() + timedelta(days=2),
            notes="Excluir",
        )
        url = reverse("consultation-detail", args=[consultation.id])
        r = self.client.delete(url)
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Consultation.objects.filter(id=consultation.id).exists())

    def test_create_with_past_datetime(self):
        payload = self.valid_payload.copy()
        payload["datetime"] = (timezone.now() - timedelta(days=1)).isoformat()
        r = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("A data/hora da consulta não pode ser no passado", str(r.data))

    def test_unauthorized_access(self):
        self.client.credentials()  # remove o token
        r = self.client.get(self.list_url)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_expired_token_access(self):
        # Create an expired token by manipulating the timestamp
        refresh = RefreshToken.for_user(self.user)
        refresh.set_exp(lifetime=timedelta(seconds=-1))  # Already expired
        expired_token = str(refresh.access_token)
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {expired_token}")
        r = self.client.get(self.list_url)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_token_format(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalid_token_format")
        r = self.client.get(self.list_url)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_missing_authorization_header(self):
        self.client.credentials(HTTP_AUTHORIZATION="")
        r = self.client.get(self.list_url)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_consultation_with_invalid_datetime_format(self):
        payload = self.valid_payload.copy()
        payload["datetime"] = "invalid-datetime-format"
        r = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_consultation_with_missing_required_fields(self):
        payload = {"notes": "Apenas notas"}
        r = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("professional", str(r.data))
        self.assertIn("datetime", str(r.data))

    def test_update_nonexistent_consultation(self):
        url = reverse("consultation-detail", args=[9999])
        r = self.client.patch(url, {"notes": "Teste"}, format="json")
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_nonexistent_consultation(self):
        url = reverse("consultation-detail", args=[9999])
        r = self.client.delete(url)
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_access_with_deleted_user_token(self):
        # Create a token for a user that will be deleted
        temp_user = User.objects.create_user(username="temp", password="123456")
        refresh = RefreshToken.for_user(temp_user)
        token = str(refresh.access_token)
        
        # Delete the user
        temp_user.delete()
        
        # Try to access with the token
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        r = self.client.get(self.list_url)
        self.assertEqual(r.status_code, status.HTTP_401_UNAUTHORIZED)