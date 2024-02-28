import pycountry
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.gis.db import models as geo_models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from user.manager.user_manager import UserManager
from django.utils.translation import gettext_lazy as _
import uuid
from user.utilities import (
    USER_GENDER_CHOICES,
    USER_REGISTER_TYPE_OPTIONS,
    USER_REGISTER_SYSTEM_TYPE,
    USER_TABLE_NAME,
)
from user.utilities.crypto_utilities import CryptoUtilities


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=20, choices=USER_GENDER_CHOICES)
    dob = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    email = models.EmailField(max_length=70, unique=True)
    username = models.CharField(max_length=70, unique=True)

    coordinates = geo_models.PointField()
    country_code = models.CharField(
        max_length=2, help_text=_('to country code like "EG", "US"')
    )

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    registered_by = models.CharField(
        max_length=30,
        choices=USER_REGISTER_TYPE_OPTIONS,
        default=USER_REGISTER_SYSTEM_TYPE,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    _crypto_token = models.TextField(editable=False, null=True, blank=True)
    two_factor_auth_enabled = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def save(self, *args, **kwargs):
        if not self._crypto_token:
            self._crypto_token = CryptoUtilities.generate_encrypted_key()
        return super().save(*args, **kwargs)

    @property
    def crypto_key(self):
        return CryptoUtilities.decrypt(cipher=self._crypto_token)

    def clean(self):
        country = pycountry.countries.get(alpha_2=self.country_code)
        if not country:
            raise ValidationError(f"country code of '{self.country_code}' not valid")
        self.country_code = country.alpha_2

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        db_table = USER_TABLE_NAME

    def __str__(self) -> str:
        return f"{self.username} || {self.email}"

    def __repr__(self) -> str:
        return f"{self.username} || {self.email}"
