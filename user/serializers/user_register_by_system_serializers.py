from rest_framework import serializers
import re
import pycountry
from user.querysets.otp_queryset import OTPQuerySet
from user.querysets.register_queryset import UserRegisterQueryset
from user.utilities.user_utilities import (
    USER_GENDER_CHOICES,
    get_point_from_coordinates,
)


class RegisterBySystemSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    gender = serializers.ChoiceField(choices=USER_GENDER_CHOICES)
    country_code = serializers.CharField(max_length=2)
    dob = serializers.DateField(allow_null=True)
    bio = serializers.CharField(allow_null=True, allow_blank=True)
    email = serializers.EmailField()
    username = serializers.CharField()
    lng = serializers.FloatField(min_value=-180, max_value=180)
    lat = serializers.FloatField(min_value=-90, max_value=90)
    password = serializers.CharField(min_length=8)
    confirm_password = serializers.CharField(min_length=8)

    def validate(self, attrs):
        attrs["country_code"] = self._validate_country_code(attrs["country_code"])
        self._validate_password(attrs["password"], attrs["confirm_password"])
        self._validate_strong_password(attrs["password"])
        self._validate_email_exists(attrs["email"])
        self._validate_username_exists(attrs["username"])
        self._set_coordinates(attrs)
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        self._delete_keys_will_not_be_saved(data)
        return UserRegisterQueryset.create_user(data)

    @staticmethod
    def _delete_keys_will_not_be_saved(attrs):
        del attrs["confirm_password"]
        del attrs["lat"]
        del attrs["lng"]

    @staticmethod
    def _set_coordinates(attrs):
        attrs["coordinates"] = get_point_from_coordinates(attrs["lng"], attrs["lat"])

    @staticmethod
    def _validate_email_exists(email):
        if UserRegisterQueryset.is_email_exists(email):
            raise serializers.ValidationError(
                {"email_exists": f"email '{email}' is already exists"}
            )

    @staticmethod
    def _validate_username_exists(username):
        if UserRegisterQueryset.is_username_exists(username):
            raise serializers.ValidationError(
                {"username_exists": f"username '{username}' is already exists"}
            )

    @staticmethod
    def _validate_country_code(country_code):
        country = pycountry.countries.get(alpha_2=country_code)
        if not country:
            raise serializers.ValidationError(
                f"country code of '{country_code}' not valid"
            )
        return country.alpha_2

    @staticmethod
    def _validate_password(password, confirm_password):
        if password != confirm_password:
            raise serializers.ValidationError(
                {"password_and_confirm_password_mismatch": "password and confirm password not the same"}
            )

    @staticmethod
    def _validate_strong_password(password):
        errors = []
        # Check if password contains digits
        if not re.search(r"[a-z]+", password):
            errors.append("password must contains small letters 'a-z'")
        # Check if password contains digits
        if not re.search(r"[0-9]+", password):
            errors.append("password must contains digits '0-9'")

        # Check if password contains uppercase letters
        if not re.search(r"[A-Z]+", password):
            errors.append("password must contains capital letters 'A-Z'")

        # Check if password contains special characters
        if not re.search(r"[!@#$%^&*()\-_=+{}[\]|\\:;\"'<>?,./]+", password):
            errors.append("password must contains special characters likes '@!%$#'")

        if errors:
            raise serializers.ValidationError({"password_not_strong": errors})


class ResendOTPSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(max_length=70)

    def validate(self, attrs):
        username_or_email = attrs["username_or_email"]
        user, is_email = UserRegisterQueryset.get_user_by_email_or_username(
            username_or_email, ["id", "email", "is_active"]
        )
        error = (
            f"user with email '{username_or_email}' not exists"
            if is_email
            else f"user with username '{username_or_email}' not exists"
        )
        if not user:
            raise serializers.ValidationError({"user_not_exists": error})

        if user.get("is_active"):
            raise serializers.ValidationError(
                {
                    "user_already_activated": f"user with email '{user.get('email')} already activated'"
                }
            )
        attrs["user"] = user
        return attrs


class VerifyEmailSerializer(ResendOTPSerializer):
    code = serializers.IntegerField(min_value=100000, max_value=999999)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        code = attrs["code"]

        invalid, expired = OTPQuerySet.is_code_is_invalid_or_expired(
            user_id=attrs.get("user").get("id"), code=code
        )
        if invalid:
            raise serializers.ValidationError(
                {"invalid_otp_code": f"code '{code}' is not valid"}
            )
        if expired:
            raise serializers.ValidationError(
                {"expired_otp_code": f"code '{code}' is expired"}
            )
        return attrs

    def save(self, **kwargs):
        UserRegisterQueryset.activate_user(self.validated_data.get("user").get("id"))
        return self.validated_data.get("user")
