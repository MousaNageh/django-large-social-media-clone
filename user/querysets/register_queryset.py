from django.contrib.auth import get_user_model


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
