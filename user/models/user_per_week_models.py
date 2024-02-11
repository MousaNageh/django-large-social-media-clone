from django.db import models
from django.utils.translation import gettext_lazy as _
from user.utilities import PG_USER_PER_WEEK_MATERIALIZED_VIEW_NAME
from django.contrib.postgres.fields import JSONField


class UserPerWeek(models.Model):
    week = models.DateField()
    user_number = models.IntegerField()
    counties = models.TextField()

    class Meta:
        managed = False
        verbose_name = _('User per week statistics')
        verbose_name_plural = _('User per week statistics')
        db_table = PG_USER_PER_WEEK_MATERIALIZED_VIEW_NAME
        ordering = ['-week']
