from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils.timezone import timedelta
from django.db import IntegrityError
from user.models import OTP
from user.tests.datasets.user_datasets import get_user_object
from user.utilities import USER_OPT_DURATION


class OTPModelTestCase(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(**get_user_object())

    def test_otp_creation(self):
        otp = OTP.objects.create(user=self.user, code=123456)
        self.assertTrue(OTP.objects.filter(user=self.user).exists())
        self.assertEqual(123456, otp.code)
        self.assertTrue(OTP.objects.filter(user=self.user, code=123456).exists())

    def test_otp_uniqueness(self):
        OTP.objects.create(user=self.user, code=123456)
        with self.assertRaises(IntegrityError):
            OTP.objects.create(user=self.user, code=654321)

    def test_otp_code_range(self):
        otp = OTP.objects.create(user=self.user, code=123456)
        self.assertTrue(100000 <= otp.code <= 999999)

    def test_otp_is_expired_property_false(self):
        otp = OTP.objects.create(
            user=self.user, code=123456, durations=timedelta(minutes=10)
        )
        self.assertFalse(otp.is_expired)

    def test_otp_is_expired_property_true(self):
        otp = OTP.objects.create(
            user=self.user, code=123456, durations=timedelta(minutes=-5)
        )
        self.assertTrue(otp.is_expired)

    def test_custom_save_method_updates_created_at(self):
        otp = OTP.objects.create(user=self.user, code=123456)
        original_created_at = otp.created_at
        otp.code = 654321
        otp.save()
        self.assertNotEqual(otp.created_at, original_created_at)

    def test_duration_default_value(self):
        otp = OTP.objects.create(user=self.user, code=123456)
        self.assertEqual(otp.durations, USER_OPT_DURATION)
