from rest_framework import serializers
from user.querysets.login_queryset import LoginQueryset


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField(max_length=70)
    password = serializers.CharField(max_length=60)

    def validate(self, attr):
        attr["user"] = self._validate_username_or_email(attr.get("username_or_email"))
        self._validate_password_match(attr["user"], attr.get("password"))
        self._validate_user_is_active(attr["user"])
        self._validate_user_agent(self.context.get("request"))
        return attr

    @staticmethod
    def _validate_username_or_email(username_or_email):
        user, is_email = LoginQueryset.get_user_by_username_or_email(
            username_or_email
        )
        if not user and is_email:
            raise serializers.ValidationError(
                {"email_not_exist": f"user with email {username_or_email} not exists"}
            )
        if not user and not is_email:
            raise serializers.ValidationError(
                {
                    "username_not_exist": f"user with username {username_or_email} not exists"
                }
            )
        return user

    @staticmethod
    def _validate_password_match(user, password):
        if not user.check_password(password):
            raise serializers.ValidationError(
                {
                    "login_error": "user with this credentials does not match"
                }
            )

    @staticmethod
    def _validate_user_is_active(user):
        if not user.is_active:
            raise serializers.ValidationError(
                {
                    "user_not_verified": "user with this credentials is not verified"
                }
            )
    @staticmethod
    def _validate_user_agent(request):
        if not request.META.get('HTTP_USER_AGENT'):
            raise serializers.ValidationError(
                {
                    "not_allowed": "you are not allowed to login"
                }
            )

    def save(self):
        user = LoginQueryset.set_login_data(user=self.validated_data.get("user"), request=self.context.get("request"))
        return user
