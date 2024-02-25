from user.models import TwoFactorAuthenticationByPhone, TwoFactorAuthenticationByEmail
from user.utilities import is_email


class TwoFactorAuthQuerySet:
    @classmethod
    def create_2fa(cls, email_or_phone, user):
        model = (
            cls._get_model(email_or_phone)
            if email_or_phone
            else TwoFactorAuthenticationByEmail
        )
        fields = cls._get_fields(user=user, email_or_phone=email_or_phone)
        return model.objects.create(**fields)

    @classmethod
    def is_created_or_activated(cls, email_or_phone, user):
        model = (
            cls._get_model(email_or_phone)
            if email_or_phone
            else TwoFactorAuthenticationByEmail
        )
        fields = cls._get_fields(user=user)
        try:
            instance = model.objects.get(**fields)
            created = True
            activated = instance.is_verified
        except model.DoesNotExist:
            created = False
            activated = False
        return created, activated

    @staticmethod
    def _get_model(email_or_phone):
        return (
            TwoFactorAuthenticationByEmail
            if is_email(email_or_phone)
            else TwoFactorAuthenticationByPhone
        )

    @staticmethod
    def _get_fields(user, email_or_phone=None):
        fields = {"user": user}
        if email_or_phone:
            if is_email(email_or_phone):
                fields["email"] = email_or_phone
            else:
                fields["phone"] = email_or_phone
        return fields
