from django.db import models
from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser
from user.manager.user_manager import UserManager
from django.utils.translation import gettext_lazy as _
import uuid
from user.utilities import USER_GENDER_CHOICES


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=20, choices=USER_GENDER_CHOICES)
    dob = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    email = models.EmailField(max_length=70, unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = _("Account")
        verbose_name_plural = _("Accounts")
        db_table = "users"

    def __str__(self) -> str:
        return self.email

    def __repr__(self) -> str:
        return self.email
