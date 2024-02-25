import uuid

import pycountry
from django.db import transaction
from rest_framework import serializers
from rest_framework.status import HTTP_200_OK
from user.querysets.login_queryset import LoginQueryset
from user.querysets.register_queryset import UserRegisterQueryset
from user.utilities import (
    USER_MALE_GENDER,
    USER_REGISTER_GOOGLE_TYPE,
    get_point_from_coordinates,
)
import requests
from faker import Faker


class RegisterByGoogleSerializer(serializers.Serializer):
    token = serializers.CharField()
    lng = serializers.FloatField(min_value=-180, max_value=180)
    lat = serializers.FloatField(min_value=-90, max_value=90)
    country_code = serializers.CharField(max_length=2)

    def validate(self, attrs):
        attrs["country_code"] = self._validate_country_code(attrs["country_code"])
        google_response = self._validate_token(attrs)
        user = self._get_user_if_exists(google_response.get("email"))
        if not user:
            self._set_user_data(attrs, google_response)
        else:
            attrs["user"] = user
        return attrs

    @staticmethod
    def _validate_country_code(country_code):
        country = pycountry.countries.get(alpha_2=country_code)
        if not country:
            raise serializers.ValidationError(
                f"country code of '{country_code}' not valid"
            )
        return country.alpha_2

    @staticmethod
    def _validate_token(attrs):
        google_url = "https://oauth2.googleapis.com/tokeninfo?id_token=" + attrs.get(
            "token"
        )
        response = requests.get(google_url)
        if response.status_code == HTTP_200_OK:
            return response.json()
        else:
            raise serializers.ValidationError(
                {"google_invalid_login": "google token is invalid"}
            )

    @staticmethod
    def _get_user_if_exists(user_email):
        return LoginQueryset.get_user_by_email(user_email)

    def _set_user_data(self, attrs, google_response):
        attrs["user_data"] = {
            "email": google_response.get("email"),
            "username": self._get_user_username(google_response),
            "first_name": "",
            "last_name": "",
            "gender": USER_MALE_GENDER,
            "dob": None,
            "registered_by": USER_REGISTER_GOOGLE_TYPE,
            "coordinates": get_point_from_coordinates(attrs["lng"], attrs["lat"]),
            "country_code": attrs["country_code"],
            "password": Faker().password(length=60, special_chars=True),
            "is_active": True,
        }
        self._handle_missing_fields(attrs, google_response)

    @staticmethod
    def _handle_missing_fields(attrs, google_response):
        name = google_response.get("name")
        if name:
            attrs["user_data"]["first_name"] = name.split(" ")[0]
            if len(name.split(" ")) > 1:
                attrs["user_data"]["last_name"] = name.split(" ")[1]
        else:
            attrs["user_data"]["last_name"] = "no last name"
            attrs["user_data"]["first_name"] = "no first name"

    @staticmethod
    def _get_user_username(google_response):
        return "-".join(
            [
                google_response.get("name", "").replace(" ", "-"),
                str(uuid.uuid4()),
            ]
        )

    def save(self, **kwargs):
        user = self.validated_data.get("user")
        with transaction.atomic():
            if not user:
                user = UserRegisterQueryset.create_user(
                    self.validated_data.get("user_data")
                )
            LoginQueryset.set_login_data(user, self.context.get("request"))
        return user
