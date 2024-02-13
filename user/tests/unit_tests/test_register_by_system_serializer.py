from django.contrib.auth import get_user_model
from django.test import TestCase
from user.serializers import RegisterBySystemSerializer
from user.tests.datasets.serializers_datasets import (
    get_register_by_system_serializer_data,
)
from user.tests.datasets.serializers_datasets import get_user_object


class RegisterBySystemSerializerTest(TestCase):

    def setUp(self):
        self.valid_data = get_register_by_system_serializer_data()

    def test_valid_data_submission(self):
        serializer = RegisterBySystemSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.errors, {})

    def test_weak_password(self):
        data = {**self.valid_data}
        data["password"] = data["confirm_password"] = "XXXXXXXXXXXXX"
        serializer = RegisterBySystemSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password_not_strong", serializer.errors)

    def test_password_and_confirm_password_mismatch(self):
        data = {**self.valid_data}
        data["confirm_password"] = "XXXXXXXXXXXXX"
        serializer = RegisterBySystemSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("password_and_confirm_password_mismatch", serializer.errors)

    def test_invalid_email_format(self):
        serializer = RegisterBySystemSerializer(
            data={**self.valid_data, "email": "invalid_email"}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_existing_email(self):
        user = self._create_user()
        serializer = RegisterBySystemSerializer(
            data={**self.valid_data, "email": user.email}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("email_exists", serializer.errors)

    def test_existing_username(self):
        user = self._create_user()
        serializer = RegisterBySystemSerializer(
            data={**self.valid_data, "username": user.username}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("username_exists", serializer.errors)

    def test_invalid_gender(self):
        serializer = RegisterBySystemSerializer(
            data={**self.valid_data, "gender": "invalid_gender"}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn("gender", serializer.errors)

    def test_date_of_birth_allows_null(self):
        data = {
            **self.valid_data,
            "dob": None,
        }
        serializer = RegisterBySystemSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_bio_allows_null_and_blank(self):
        data = {
            **self.valid_data,
            "bio": None,
        }
        serializer = RegisterBySystemSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        data["bio"] = ""
        serializer = RegisterBySystemSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_longitude_out_of_range(self):
        data = {
            **self.valid_data,
            "lng": 200,
        }
        serializer = RegisterBySystemSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("lng", serializer.errors)

    def test_latitude_out_of_range(self):
        data = {
            **self.valid_data,
            "lat": -100,
        }
        serializer = RegisterBySystemSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("lat", serializer.errors)

    def test_longitude_latitude_conversion_to_coordinates(self):
        serializer = RegisterBySystemSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertIsNotNone(user.coordinates)
        self.assertEqual(user.coordinates.x, self.valid_data["lng"])
        self.assertEqual(user.coordinates.y, self.valid_data["lat"])

    def test_serializer_save(self):
        serializer = RegisterBySystemSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.email, self.valid_data["email"])
        self.assertEqual(user.username, self.valid_data["username"])
        self.assertEqual(user.first_name, self.valid_data["first_name"])
        self.assertEqual(user.last_name, self.valid_data["last_name"])
        self.assertEqual(user.gender, self.valid_data["gender"])
        self.assertEqual(user.country_code, self.valid_data["country_code"])
        self.assertEqual(user.bio, self.valid_data["bio"])
        self.assertEqual(user.dob.strftime("%Y-%m-%d"), self.valid_data["dob"])
        self.assertEqual(user.is_active, False)

    def _create_user(self):
        user_data = get_user_object()
        user_model = get_user_model()
        user = user_model.objects.create_user(**user_data)
        return user
