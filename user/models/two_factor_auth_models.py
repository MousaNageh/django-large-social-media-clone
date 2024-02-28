from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
import uuid


class TwoFactorAuthenticationByEmail(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(
        get_user_model(), related_name="user_2fa_email", on_delete=models.CASCADE
    )
    email = models.EmailField(null=True, blank=True)
    use_current_email = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.use_current_email and not self.email:
            raise ValidationError(
                _("email can not be empty with no selection for 'use current email")
            )

    class Meta:
        unique_together = [("user", "email")]
        verbose_name = _("email two factor auth")
        verbose_name_plural = _("email two factor auth")

    def __str__(self):
        return str(self.email)


class TwoFactorAuthenticationByPhone(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(
        get_user_model(), related_name="user_2fa_phone", on_delete=models.CASCADE
    )
    phone = PhoneNumberField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [("user", "phone")]

    def __str__(self):
        return str(self.phone)
