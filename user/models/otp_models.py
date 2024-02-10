from django.contrib.auth import get_user_model
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from user.utilities import USER_OPT_DURATION


class OTP(models.Model):
    user = models.OneToOneField(
        get_user_model(), related_name="user_otp", on_delete=models.CASCADE
    )
    code = models.PositiveIntegerField()
    durations = models.DurationField(default=USER_OPT_DURATION)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("OTP")
        verbose_name_plural = _("OTP")
        db_table = "otp"
        indexes = [
            models.Index(fields=["user_id", "code"], name="otp_user_id_code_idx")
        ]

    @property
    def is_expired(self):
        return now() > self.created_at + self.durations

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if self.pk:
            self.created_at = now()
        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
