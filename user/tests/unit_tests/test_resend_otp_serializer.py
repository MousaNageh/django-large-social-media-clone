from django.contrib.auth import get_user_model
from django.test import TestCase
from user.serializers import ResendOTPSerializer
from user.tests.datasets.user_datasets import get_user_object


class ResendOTPSerializerTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.active_user = get_user_model().objects.create_user(**get_user_object(is_active=True))
        cls.inactive_user = get_user_model().objects.create_user(**get_user_object(is_active=False))

    def test_valid_username_input(self):
        serializer = ResendOTPSerializer(data={'username_or_email': self.inactive_user.username})
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_valid_email_input(self):
        serializer = ResendOTPSerializer(data={'username_or_email': self.inactive_user.email})
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_nonexistent_username(self):
        serializer = ResendOTPSerializer(data={'username_or_email': 'nonexistentUser'})
        self.assertFalse(serializer.is_valid())
        self.assertIn('user_not_exists', serializer.errors)

    def test_nonexistent_email(self):
        serializer = ResendOTPSerializer(data={'username_or_email': 'nonexistent@example.com'})
        self.assertFalse(serializer.is_valid())
        self.assertIn('user_not_exists', serializer.errors)

    def test_user_already_activated_with_username(self):
        serializer = ResendOTPSerializer(data={'username_or_email': self.active_user.username})
        self.assertFalse(serializer.is_valid())
        self.assertIn('user_already_activated', serializer.errors)

    def test_user_already_activated_with_email(self):
        serializer = ResendOTPSerializer(data={'username_or_email': self.active_user.email})
        self.assertFalse(serializer.is_valid())
        self.assertIn('user_already_activated', serializer.errors)

    def test_maximum_length_exceeded(self):
        long_input = 'a' * 71
        serializer = ResendOTPSerializer(data={'username_or_email': long_input})
        self.assertFalse(serializer.is_valid())
        self.assertIn('username_or_email', serializer.errors)

    def test_empty_username_or_email(self):
        serializer = ResendOTPSerializer(data={'username_or_email': ''})
        self.assertFalse(serializer.is_valid())
        self.assertIn('username_or_email', serializer.errors)

    def test_serializer_with_blank_input(self):
        serializer = ResendOTPSerializer(data={'username_or_email': ' '})
        self.assertFalse(serializer.is_valid())
        self.assertIn('username_or_email', serializer.errors)

    def test_injection_of_additional_fields(self):
        data = {'username_or_email': self.inactive_user.email, 'unexpected_field': 'unexpected_value'}
        serializer = ResendOTPSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn('unexpected_field', serializer.validated_data)
