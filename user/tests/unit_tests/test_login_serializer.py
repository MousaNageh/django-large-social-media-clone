from django.test import TestCase
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.test.client import RequestFactory

from user.models import UserActivity
from user.serializers.login_serializers import LoginSerializer
from user.tests.datasets.user_datasets import get_user_object

User = get_user_model()


class LoginSerializerTestCase(TestCase):

    def setUp(self):
        self.user_data = get_user_object()
        self.user = User.objects.create_user(**self.user_data)
        self.factory = RequestFactory()
        self.request = self.factory.post(
            "/",
            **{
                "HTTP_USER_AGENT": "Mozilla/5.0",
                "REMOTE_ADDR": "127.0.0.1",
            }
        )

    def test_valid_login_with_username(self):
        data = {
            "username_or_email": self.user.username,
            "password": self.user_data.get("password"),
        }
        serializer = LoginSerializer(data=data, context={"request": self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_valid_login_with_email(self):
        data = {
            "username_or_email": self.user.email,
            "password": self.user_data.get("password"),
        }
        serializer = LoginSerializer(data=data, context={"request": self.request})
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_valid_login_without_meta_data(self):
        data = {
            "username_or_email": self.user.email,
            "password": self.user_data.get("password"),
        }
        serializer = LoginSerializer(
            data=data, context={"request": self.factory.get("/")}
        )
        serializer.is_valid()
        self.assertIn("not_allowed", serializer.errors)

    def test_non_existent_email(self):
        data = {
            "username_or_email": "nonexistent@example.com",
            "password": self.user_data.get("password"),
        }
        serializer = LoginSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_non_existent_username(self):
        data = {
            "username_or_email": "nonexistusername",
            "password": self.user_data.get("password"),
        }
        serializer = LoginSerializer(data=data)
        with self.assertRaises(ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_save_method_updates_last_login(self):
        data = {
            "username_or_email": self.user.email,
            "password": self.user_data.get("password"),
        }
        serializer = LoginSerializer(data=data, context={"request": self.request})
        if serializer.is_valid():
            user = serializer.save()
            self.assertIsNotNone(user.last_login)

    def test_save_method_updates_user_activity(self):
        data = {
            "username_or_email": self.user.username,
            "password": self.user_data.get("password"),
        }
        serializer = LoginSerializer(data=data, context={"request": self.request})
        if serializer.is_valid():
            user = serializer.save()
            activities = UserActivity.objects.filter(user=user)
            self.assertTrue(len(activities))
            user_activity = activities.last()
            self.assertEqual(user_activity.user_agent, "Mozilla/5.0")
            self.assertEqual(user_activity.ip_address, "127.0.0.1")
