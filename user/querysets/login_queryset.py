from uuid import UUID

from django.contrib.auth import get_user_model
from django.utils.timezone import now
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

from user.querysets.user_activity_queryset import UserActivityQuerySet
from user.utilities import is_email


class LoginQueryset:
    model = get_user_model()

    @classmethod
    def get_user_by_username_or_email(cls, email_or_username):
        input_type_email = is_email(email_or_username)
        get_user_method = (
            cls.get_user_by_email if input_type_email else cls.get_user_by_username
        )
        return get_user_method(email_or_username), input_type_email

    @classmethod
    def get_user_by_email(cls, email):
        return cls.get_user_by_fields({"email": email})

    @classmethod
    def get_user_by_username(cls, username):
        return cls.get_user_by_fields({"username": username})

    @classmethod
    def get_user_by_fields(cls, fields_dict):
        try:
            return cls.model.objects.get(**fields_dict)
        except cls.model.DoesNotExist:
            return None

    @staticmethod
    def update_login_date_for_user(user):
        user.last_login = now()
        user.save(update_fields=["last_login"])
        return user

    @classmethod
    def set_login_data(cls, user, request):
        with transaction.atomic():
            cls.update_login_date_for_user(user)
            UserActivityQuerySet.create(user, request)
        return user

    @staticmethod
    def get_token_for_user(user, extra_fields=["id", "email", "username"]):
        token = RefreshToken.for_user(user)
        for field in extra_fields:
            value = getattr(user, field)
            if isinstance(value, UUID):
                value = str(value)
            token[field] = value

        return {"refresh": str(token), "access": str(token.access_token)}
