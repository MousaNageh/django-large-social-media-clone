from django.contrib.auth import get_user_model

from user.utilities import is_email


class UserRegisterQueryset:

    @classmethod
    def is_email_exists(cls, email):
        return cls._is_field_exits({"email": email})

    @classmethod
    def is_username_exists(cls, username):
        return cls._is_field_exits({"username": username})

    @staticmethod
    def _is_field_exits(field_dict):
        user_model = get_user_model()
        try:
            user_model.objects.values(*list(field_dict.keys())).get(**field_dict)
            return True
        except user_model.DoesNotExist:
            return False

    @staticmethod
    def create_user(data):
        user_model = get_user_model()
        return user_model.objects.create_user(**data)

    @staticmethod
    def activate_user(user_id):
        return get_user_model().objects.filter(id=user_id).update(is_active=True)

    @staticmethod
    def get_user_by_email_or_username(email_or_username, values=["id", "email"]):
        user_model = get_user_model()
        input_is_email = is_email(email_or_username)
        data_dict = (
            {"email": email_or_username}
            if input_is_email
            else {"username": email_or_username}
        )
        try:
            return (
                user_model.objects.values(*values).get(**data_dict),
                input_is_email,
            )
        except user_model.DoesNotExist:
            return "", input_is_email
