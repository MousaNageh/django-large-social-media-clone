from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from user.models import OTP
from user.serializers import VerifyEmailSerializer
from user.tests.datasets.user_datasets import get_user_object


class VerifyEmailSerializerTestCase(TestCase):

    def setUp(self):
        self.user = self.user = get_user_model().objects.create_user(**get_user_object(is_active=False))
        self.otp = OTP.objects.create(user=self.user, code=123456)

    def test_valid_code_and_email(self):
        data = {'username_or_email': self.user.email, 'code': self.otp.code}
        serializer = VerifyEmailSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_otp_code(self):
        data = {'username_or_email': self.user.email, 'code': 654321}
        serializer = VerifyEmailSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('invalid_otp_code', serializer.errors)

    def test_expired_otp_code(self):
        user = get_user_model().objects.create_user(**get_user_object(is_active=False))
        otp = OTP.objects.create(user=user, code=123456, durations=timedelta(minutes=-5))
        data = {'username_or_email': user.email, 'code': otp.code}
        serializer = VerifyEmailSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('expired_otp_code', serializer.errors)

    def test_activation_on_valid_data(self):
        data = {'username_or_email': self.user.email, 'code': self.otp.code}
        serializer = VerifyEmailSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        serializer.save()
        user = get_user_model().objects.get(id=self.user.id)
        self.assertTrue(user.is_active)
