from user.models import TwoFactorAuthenticationByPhone, TwoFactorAuthenticationByEmail
from user.querysets.otp_queryset import OTPQuerySet
from user.tasks.send_2fa_email import send_2fa_activate_email
from user.utilities import is_email
from django.db import transaction


class TwoFactorAuthQuerySet:
    @classmethod
    def create_2fa(cls, email_or_phone, user, **extra_fields):
        model = (
            cls._get_model(email_or_phone)
            if email_or_phone
            else TwoFactorAuthenticationByEmail
        )
        fields = cls._get_fields(user=user, email_or_phone=email_or_phone)
        fields |= extra_fields
        return model.objects.create(**fields)

    @classmethod
    def create_2fa_with_send_email(cls, email, user, **extra_fields):
        with transaction.atomic():
            two_auth_instance = cls.create_2fa(email, user, **extra_fields)
            opt = OTPQuerySet.create_or_replace_otp(user_id=user.id)
            if not extra_fields.get("user_current_email") and email:
                send_2fa_activate_email.delay(opt.code, email)
            return two_auth_instance

    @classmethod
    def resend_otp_email_for_user(cls, user):
        try:
            instance = TwoFactorAuthenticationByEmail.objects.get(user=user)
            if instance.email and not instance.is_verified:
                opt = OTPQuerySet.create_or_replace_otp(user_id=user.id)
                send_2fa_activate_email.delay(opt.code, instance.email)
                return instance
        except TwoFactorAuthenticationByEmail.DoesNotExist:
            return None

    @classmethod
    def is_created_or_verified(cls, email_or_phone, user):
        model = (
            cls._get_model(email_or_phone)
            if email_or_phone
            else TwoFactorAuthenticationByEmail
        )
        fields = cls._get_fields(user=user)
        try:
            instance = model.objects.get(**fields)
            created = True
            verified = instance.is_verified
        except model.DoesNotExist:
            created = False
            verified = False
        return created, verified

    @classmethod
    def get_2fa_for_email(cls, user):
        fields = cls._get_fields(user=user)
        try:
            return TwoFactorAuthenticationByEmail.objects.get(**fields)
        except TwoFactorAuthenticationByEmail.DoesNotExist:
            return None

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

    @staticmethod
    def activate_2fa(instance):
        instance.is_verified = True
        instance.save(update_fields=["is_verified"])
        return instance
