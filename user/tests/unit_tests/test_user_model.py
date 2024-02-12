from django.db import IntegrityError
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from user.tests.datasets.user_datasets import get_user_object


class UserModelTests(TestCase):

    def test_create_user_with_valid_data(self):
        user_dict = get_user_object()
        user_model = get_user_model()
        user = user_model.objects.create_user(**user_dict)
        self.assertEqual(user.email, user_dict.get("email"))
        self.assertTrue(user.check_password(user_dict.get("password")))
        self.assertEqual(user.first_name,  user_dict.get("first_name"))
        self.assertEqual(user.last_name, user_dict.get("last_name"))
        self.assertEqual(user.username, user_dict.get("username"))
        self.assertEqual(user.gender, user_dict.get("gender"))
        self.assertEqual(user.dob, user_dict.get('dob'))
        self.assertEqual(user.bio, user_dict.get('bio'))
        self.assertEqual(user.country_code, user_dict.get('country_code'))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)

    def test_user_creation_with_invalid_country_code(self):
        user_dict = get_user_object()
        user_dict["country_code"] = "XX"
        user_model = get_user_model()
        with self.assertRaises(ValidationError):
            user = user_model.objects.create_user(**user_dict)
            print(user.country_code)

    def test_email_normalization(self):
        user_dict = get_user_object()
        user_dict["email"] = "TEST@EXAMPLE.COM"
        user_model = get_user_model()
        user = user_model.objects.create_user(**user_dict)
        self.assertEqual(user.email, 'test@example.com')

    def test_missing_first_name(self):
        user_model = get_user_model()
        user_dict = get_user_object()
        del user_dict["first_name"]
        with self.assertRaises(ValueError):
            user_model.objects.create_user(**user_dict)

    def test_missing_last_name(self):
        user_model = get_user_model()
        user_dict = get_user_object()
        del user_dict["last_name"]
        with self.assertRaises(ValueError):
            user_model.objects.create_user(**user_dict)

    def test_missing_username(self):
        user_model = get_user_model()
        user_dict = get_user_object()
        del user_dict["username"]
        with self.assertRaises(ValueError):
            user_model.objects.create_user(**user_dict)

    def test_missing_gender(self):
        user_model = get_user_model()
        user_dict = get_user_object()
        del user_dict["gender"]
        with self.assertRaises(ValueError):
            user_model.objects.create_user(**user_dict)

    def test_missing_invalid_gender(self):
        user_model = get_user_model()
        user_dict = get_user_object()
        user_dict["gender"] = "XX"
        with self.assertRaises(ValidationError):
            user_model.objects.create_user(**user_dict)

    def test_missing_country_code(self):
        user_model = get_user_model()
        user_dict = get_user_object()
        del user_dict["country_code"]
        with self.assertRaises(ValueError):
            user_model.objects.create_user(**user_dict)

    def test_superuser_creation_with_proper_flags(self):
        user_model = get_user_model()
        user_dict = get_user_object()
        superuser = user_model.objects.create_superuser(**user_dict)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)

    def test_password_set_for_user(self):
        user_model = get_user_model()
        user_dict = get_user_object()
        user = user_model.objects.create_user(**user_dict)
        self.assertTrue(user.check_password(user_dict.get("password")))

    def test_user_string_representation(self):
        user_model = get_user_model()
        user_dict = get_user_object()
        user = user_model.objects.create_user(**user_dict)
        self.assertEqual(str(user), f"{user_dict.get("username")} || {user_dict.get("email")}")

    def test_email_uniqueness(self):
        user_model = get_user_model()
        user_dict = get_user_object()
        user_model.objects.create_user(**user_dict)
        with self.assertRaises(IntegrityError):
            user_dict2 = get_user_object()
            user_dict2["email"] = user_dict["email"]
            user_model.objects.create_user(**user_dict2)

    def test_username_uniqueness(self):
        user_model = get_user_model()
        user_dict = get_user_object()
        user_model.objects.create_user(**user_dict)
        with self.assertRaises(IntegrityError):
            user_dict2 = get_user_object()
            user_dict2["username"] = user_dict["username"]
            user_model.objects.create_user(**user_dict2)
