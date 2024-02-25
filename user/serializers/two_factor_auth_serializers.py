from rest_framework import serializers
from user.models import TwoFactorAuthenticationByEmail, TwoFactorAuthenticationByPhone
from user.querysets.two_factor_auth_queryset import TwoFactorAuthQuerySet
from user.utilities import USER_REGISTER_FACEBOOK_TYPE, DEFAULT_EMAIL_DOMAIN


class TwoFactorAuthSerializerByEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwoFactorAuthenticationByEmail
        exclude = ["is_verified", "user"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_use_current_email(self, use_current_email):
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
        return use_current_email

    def validate_email(self, email):
        created, activated = TwoFactorAuthQuerySet.is_created_or_activated(
            user=self.context["request"].user, email_or_phone=email
        )
        if created:
            raise serializers.ValidationError(
                {"2fa_exists": "user already created 2fa with email"}
            )
        if activated:
            raise serializers.ValidationError(
                {"2fa_activated": "user already activated 2fa with email"}
            )
        return email

    def validate(self, attrs):
        if not attrs.get("email") and not attrs.get("use_current_email"):
            raise serializers.ValidationError(
                {"email": "email is required if no use_current_email"}
            )
        if attrs.get("email").lower() == self.context["request"].user.email.lower():
            attrs["use_current_email"] = True
            attrs["email"] = ""
        return attrs

    def save(self, **kwargs):
        if not self.validated_data.get("use_current_email"):
            pass

        super().save(**kwargs)


class TwoFactorAuthSerializerByPhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwoFactorAuthenticationByPhone
        exclude = ["is_verified", "user"]
        read_only_fields = ["id", "created_at", "updated_at"]
        write_only_fields = ["user"]

    def validate_phone(self, phone):
        created, activated = TwoFactorAuthQuerySet.is_created_or_activated(
            user=self.context["request"].user, email_or_phone=phone
        )
        if created:
            raise serializers.ValidationError(
                {"2fa_exists": "user already created 2fa with phone"}
            )
        if activated:
            raise serializers.ValidationError(
                {"2fa_activated": "user already activated 2fa with phone"}
            )
