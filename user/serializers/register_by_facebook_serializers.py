import pycountry
from django.db import transaction
from rest_framework import serializers
from rest_framework.status import HTTP_200_OK
from user.querysets.login_queryset import LoginQueryset
from user.querysets.register_queryset import UserRegisterQueryset
from user.utilities import (
    USER_MALE_GENDER,
    USER_REGISTER_FACEBOOK_TYPE,
    get_point_from_coordinates,
)
import requests
from faker import Faker


class RegisterByFacebookSerializer(serializers.Serializer):
    token = serializers.CharField()
    user_id = serializers.CharField()
    lng = serializers.FloatField(min_value=-180, max_value=180)
    lat = serializers.FloatField(min_value=-90, max_value=90)
    country_code = serializers.CharField(max_length=2)

    def validate(self, attrs):
        attrs["country_code"] = self._validate_country_code(attrs["country_code"])
        facebook_response = self._validate_token(attrs)
        user = self._get_user_if_exists(self._get_user_email(facebook_response))
        if not user:
            self._set_user_data(attrs, facebook_response)
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
        user_facebook_id = attrs["user_id"]
        token = attrs["token"]
        facebook_url = (
            f"https://graph.facebook.com/{user_facebook_id}?"
            f"fields=id,name,gender,birthday,email,first_name,last_name&access_token={token}"
        )
        response = requests.get(facebook_url)
        if response.status_code == HTTP_200_OK:
            return response.json()
        else:
            raise serializers.ValidationError(
                {"facebook_invalid_login": "user id or facebook token is invalid"}
            )

    @staticmethod
    def _get_user_if_exists(user_email):
        return LoginQueryset.get_user_by_email(user_email)

    def _set_user_data(self, attrs, facebook_response):
        attrs["user_data"] = {
            "email": (
                self._get_user_email(facebook_response)
                if not facebook_response.get("email")
                else facebook_response.get("email")
            ),
            "username": self._get_user_username(facebook_response),
            "first_name": facebook_response.get("first_name", ""),
            "last_name": facebook_response.get("last_name", ""),
            "gender": facebook_response.get("gender", USER_MALE_GENDER),
            "dob": facebook_response.get("birthday"),
            "registered_by": USER_REGISTER_FACEBOOK_TYPE,
            "coordinates": get_point_from_coordinates(attrs["lng"], attrs["lat"]),
            "country_code": attrs["country_code"],
            "password": Faker().password(length=60, special_chars=True),
            "is_active": True
        }
        self._handle_missing_fields(attrs, facebook_response)

    @staticmethod
    def _handle_missing_fields(attrs, facebook_response):
        name = facebook_response.get("name")
        if attrs["user_data"].get("first_name"):
            if name:
                attrs["user_data"]["first_name"] = name.split(" ")[0]
            else:
                attrs["user_data"]["first_name"] = "no first name"

        if not not attrs["user_data"].get("last_name"):
            if name and len(name.split(" ")) > 1:
                attrs["user_data"]["last_name"] = name.split(" ")[1]
            else:
                attrs["user_data"]["last_name"] = "no last name"

    @staticmethod
    def _get_user_email(facebook_response):
        email = (
            facebook_response.get("email")
            if facebook_response.get("email")
            else facebook_response.get("id") + "@social.com"
        )
        return email

    @staticmethod
    def _get_user_username(facebook_response):
        return "-".join(
            [
                facebook_response.get("name", "").replace(" ", "-"),
                str(facebook_response.get("id")),
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
