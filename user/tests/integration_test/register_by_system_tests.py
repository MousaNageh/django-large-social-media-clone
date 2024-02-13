from datetime import timedelta

from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from user.models import OTP
from user.tests.datasets.serializers_datasets import (
    get_register_by_system_serializer_data,
)
from user.tests.datasets.user_datasets import get_user_object


class RegisterBySystemIntegrationTestCase(APITestCase):

    def setUp(self):
        self.register_data = get_register_by_system_serializer_data()
        self.user_model = get_user_model()
        self.url = reverse("register-by-system-api")
        self.user_data = get_user_object()

    def test_full_user_creation_and_activation_with_email(self):
        response = self.client.post(self.url, self.register_data)
        created_email = response.json().get("email")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        code = self._get_otp_by_email(created_email).code
        activation_data = {"username_or_email": created_email, "code": code}
        activation_response = self.client.patch(self.url, activation_data)
        self.assertEqual(activation_response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user_model.objects.get(email=created_email).is_active)

    def test_full_user_creation_and_activation_with_username(self):
        response = self.client.post(self.url, self.register_data)
        created_username = response.json().get("username")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        code = self._get_otp_by_username(created_username).code
        activation_data = {"username_or_email": created_username, "code": code}
        activation_response = self.client.patch(self.url, activation_data)
        self.assertEqual(activation_response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            self.user_model.objects.get(username=created_username).is_active
        )

    def test_full_user_creation_and_activation_with_email_after_resend_code(self):
        response = self.client.post(self.url, self.register_data)
        created_email = response.json().get("email")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        opt = self._get_otp_by_email(created_email)
        old_code = opt.code
        resend_code_response = self._send_resend_code_request(created_email)
        self.assertEqual(resend_code_response.status_code, status.HTTP_200_OK)
        new_code = self._get_otp_by_email(created_email).code
        self.assertNotEqual(old_code, new_code)
        activation_data = {"username_or_email": created_email, "code": new_code}
        activation_response = self.client.patch(self.url, activation_data)
        self.assertEqual(activation_response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.user_model.objects.get(email=created_email).is_active)

    def test_full_user_creation_and_activation_with_username_after_resend_code(self):
        response = self.client.post(self.url, self.register_data)
        created_username = response.json().get("username")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        old_code = self._get_otp_by_username(created_username).code
        resend_code_response = self.client.put(
            self.url, {"username_or_email": created_username}
        )
        self.assertEqual(resend_code_response.status_code, status.HTTP_200_OK)
        new_code = self._get_otp_by_username(created_username).code
        self.assertNotEqual(old_code, new_code)
        activation_data = {"username_or_email": created_username, "code": new_code}
        activation_response = self.client.patch(self.url, activation_data)
        self.assertEqual(activation_response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            self.user_model.objects.get(username=created_username).is_active
        )

    def test_full_user_creation_and_activation_with_username_and_with_invalid_code(self):
        response = self.client.post(self.url, self.register_data)
        created_username = response.json().get("username")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        otp = self._get_otp_by_username(created_username)
        old_code = otp.code
        self._change_otp_code(otp)
        activation_data = {"username_or_email": created_username, "code": old_code}
        activation_response = self.client.patch(self.url, activation_data)
        self.assertEqual(activation_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("invalid_otp_code", activation_response.json())

    def test_full_user_creation_and_activation_with_username_and_with_expired_code(
        self,
    ):
        response = self.client.post(self.url, self.register_data)
        created_username = response.json().get("username")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        otp = self._get_otp_by_username(created_username)
        old_code = otp.code
        self._change_otp_duration(otp)
        activation_data = {"username_or_email": created_username, "code": old_code}
        activation_response = self.client.patch(self.url, activation_data)
        self.assertEqual(activation_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("expired_otp_code", activation_response.json())

    def test_full_user_creation_and_activation_with_email_and_with_expired_code(self):
        response = self.client.post(self.url, self.register_data)
        created_email = response.json().get("email")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        otp = self._get_otp_by_email(created_email)
        old_code = otp.code
        self._change_otp_duration(otp)
        activation_data = {"username_or_email": created_email, "code": old_code}
        activation_response = self.client.patch(self.url, activation_data)
        self.assertEqual(activation_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("expired_otp_code", activation_response.json())

    def test_full_user_creation_and_activation_with_email_and_with_invalid_code(
        self,
    ):
        response = self.client.post(self.url, self.register_data)
        created_email = response.json().get("email")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        otp = self._get_otp_by_email(created_email)
        old_code = otp.code
        self._change_otp_code(otp)
        activation_data = {"username_or_email": created_email, "code": old_code}
        activation_response = self.client.patch(self.url, activation_data)
        self.assertEqual(activation_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("invalid_otp_code", activation_response.json())

    def test_full_user_creation_and_activation_with_username_resend_code(self):
        response = self.client.post(self.url, self.register_data)
        created_username = response.json().get("username")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        code = self._get_otp_by_username(created_username).code
        activation_data = {"username_or_email": created_username, "code": code}
        activation_response = self.client.patch(self.url, activation_data)
        self.assertEqual(activation_response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            self.user_model.objects.get(username=created_username).is_active
        )

    def test_user_created_success(self):
        response = self.client.post(self.url, self.register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            self.user_model.objects.filter(
                email=self.register_data.get("email")
            ).exists()
        )
        self.assertTrue(
            self.user_model.objects.filter(
                username=self.register_data.get("username")
            ).exists()
        )

    def test_register_user_with_existing_email(self):
        self.user_model.objects.create_user(**self.user_data)
        data = {**self.register_data, "email": self.user_data.get("email")}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email_exists", response.json())

    def test_register_user_with_existing_username(self):
        self.user_model.objects.create_user(**self.user_data)
        data = {**self.register_data, "username": self.user_data.get("username")}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username_exists", response.json())

    def test_otp_created_after_create_user(self):
        response = self.client.post(self.url, self.register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            OTP.objects.filter(user__email=response.json().get("email")).exists()
        )

    def test_user_already_activated(self):
        response = self.client.post(self.url, self.register_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        email = response.json().get("email")
        user = self.user_model.objects.get(email=email)
        user.is_active = True
        user.save()
        activation_data = {"username_or_email": email, "code": self._get_otp_by_email(email).code}
        activation_response = self.client.patch(self.url, activation_data)
        self.assertEqual(activation_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("user_already_activated", activation_response.json())

    def _send_resend_code_request(self, username_or_email):
        return self.client.put(
            self.url, {"username_or_email": username_or_email}
        )

    @staticmethod
    def _change_otp_code(otp):
        old_code = otp.code
        otp.code = old_code - 1
        otp.save()
        return otp

    @staticmethod
    def _change_otp_duration(otp):
        otp.durations = timedelta(minutes=-11)
        otp.save()
        return otp

    @staticmethod
    def _get_otp_by_email(email):
        return OTP.objects.get(user__email=email)

    @staticmethod
    def _get_otp_by_username(username):
        return OTP.objects.get(user__username=username)