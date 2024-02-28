from rest_framework import serializers
from user.models import TwoFactorAuthenticationByEmail
from user.querysets.two_factor_auth_queryset import TwoFactorAuthQuerySet
from user.querysets.otp_queryset import OTPQuerySet
from user.utilities import USER_REGISTER_FACEBOOK_TYPE, DEFAULT_EMAIL_DOMAIN


class TwoFactorAuthSerializerByEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwoFactorAuthenticationByEmail
        exclude = ["user"]
        read_only_fields = ["id", "created_at", "updated_at", "is_verified"]

    def validate(self, attrs):
        self._validate_email(attrs.get("email"))
        self._validate_use_current_email(attrs.get("use_current_email"))
        if not attrs.get("email") and not attrs.get("use_current_email"):
            raise serializers.ValidationError(
                {"email": "email is required if no use_current_email"}
            )
        self._set_clean_data(attrs)
        return attrs

    def _set_clean_data(self, attrs):
        attrs["is_verified"] = False
        if attrs.get("email").lower() == self.context[
            "request"
        ].user.email.lower() or attrs.get("use_current_email"):
            attrs["use_current_email"] = True
            attrs["is_verified"] = True
            attrs["email"] = ""

    def _validate_use_current_email(self, use_current_email):
        if (
            self.context["request"].user.registered_by == USER_REGISTER_FACEBOOK_TYPE
            and DEFAULT_EMAIL_DOMAIN in self.context["request"].user.email
            and use_current_email
        ):
            raise serializers.ValidationError(
                {
                    "registered_by_facebook_error": f"user can set 2fa with email {self.context['request'].user.email}"
                }
            )

    def _validate_email(self, email):
        created, verified = TwoFactorAuthQuerySet.is_created_or_verified(
            user=self.context["request"].user, email_or_phone=email
        )
        if created:
            raise serializers.ValidationError(
                {"2fa_exists": "user already created 2fa with email"}
            )
        if verified:
            raise serializers.ValidationError(
                {"2fa_verified": "user already verified 2fa with email"}
            )

    def save(self, **kwargs):
        instance = TwoFactorAuthQuerySet.create_2fa_with_send_email(
            email=self.validated_data.get("email"),
            user=self.context["request"].user,
            use_current_email=self.validated_data.get("use_current_email", False),
            is_verified=self.validated_data.get("is_verified", False),
        )
        return instance


class ActivateTwoFactorAuthByEmail(serializers.Serializer):
    code = serializers.IntegerField(min_value=100000, max_value=999999, write_only=True)

    def validate(self, attrs):
        instance = TwoFactorAuthQuerySet.get_2fa_for_email(
            user=self.context["request"].user
        )
        self._validate_is_2fa_created(instance)
        self._validate_otp(self.context["request"].user.id, code=attrs["code"])
        attrs["instance"] = instance
        return attrs

    @staticmethod
    def _validate_otp(user_id, code):
        invalid, expired = OTPQuerySet.is_code_is_invalid_or_expired(
            user_id=user_id, code=code
        )
        if invalid:
            raise serializers.ValidationError(
                {"invalid_otp_code": f"code '{code}' is not valid"}
            )
        if expired:
            raise serializers.ValidationError(
                {"expired_otp_code": f"code '{code}' is expired"}
            )

    @staticmethod
    def _validate_is_2fa_created(instance):
        if not instance:
            raise serializers.ValidationError(
                {"2fa_not_exists": "user does not create 2fa"}
            )
        if instance.is_verified:
            raise serializers.ValidationError(
                {"2fa_verified": "user already verified 2fa with email"}
            )

    def save(self, **kwargs):
        self.validated_data["instance"] = TwoFactorAuthQuerySet.activate_2fa(
            self.validated_data["instance"]
        )
        return self.validated_data["instance"]

    def to_representation(self, instance):
        return {"is_verified": True}
