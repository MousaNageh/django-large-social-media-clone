import pycountry
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models, connection
from psqlextra.models import PostgresPartitionedModel
from django.utils.translation import gettext_lazy as _
from psqlextra.types import PostgresPartitioningMethod
from django.db.models.signals import pre_save
from django.dispatch import receiver
from user.utilities import ACTIVITY_TABLE_NAME, PG_CREATE_PARTITION_FUNCTION


class UserActivity(PostgresPartitionedModel):
    user = models.ForeignKey(
        get_user_model(), related_name="user_activities", on_delete=models.CASCADE
    )
    ip_address = models.GenericIPAddressField()
    country_code = models.CharField(max_length=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        country = pycountry.countries.get(alpha_2=self.country_code)
        if not country:
            raise ValidationError(f"country code of '{self.country_code}' not valid")
        self.country_code = country.alpha_2

    def __str__(self):
        return str(self.ip_address)

    class Meta:
        verbose_name = _("User activity")
        db_table = ACTIVITY_TABLE_NAME
        verbose_name_plural = _("User Activities")
        indexes = [
            models.Index(
                fields=["user", "country_code"], name="activity_user_country_index"
            )
        ]

    class PartitioningMeta:
        method = PostgresPartitioningMethod.LIST
        key = ["country_code"]


@receiver(pre_save, sender=UserActivity)
def create_partition_before_save(sender, instance, **kwargs):
    if not instance.pk:
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT {PG_CREATE_PARTITION_FUNCTION}(%s)", [instance.country_code]
            )
