from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        """Creates and saves a new user"""
        if not extra_fields.get("first_name"):
            raise ValueError(_("First name must be set"))

        if not extra_fields.get("last_name"):
            raise ValueError(_("Last name must be set"))

        if not extra_fields.get("username"):
            raise ValueError(_("username must be set"))

        if not extra_fields.get("gender"):
            raise ValueError(_("gender must be set"))

        if not email:
            raise ValueError(_("The Email must be set"))

        if not password:
            raise ValueError(_("The Password must be set"))

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        user.set_password(password)

        user.save(using=self._db)

        user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates and saves a new superuser"""
        extra_fields.update(
            {
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            }
        )
        return self.create_user(email=email, password=password, **extra_fields)

    def normalize_email(self, email):
        email = super().normalize_email(email)
        return email.lower()
