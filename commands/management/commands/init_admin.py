from django.core.management.base import BaseCommand
from django.db import IntegrityError

from user.models import User
from user.utilities import USER_MALE_GENDER


class Command(BaseCommand):
    help = "create or show admin panel user"

    def handle(self, *args, **options):
        admin_email = "admin@admin.com"
        try:
            admin = User.objects.create_superuser(
                email=admin_email,
                password="12345",
                first_name="admin",
                last_name="admin",
                gender=USER_MALE_GENDER,
            )
            admin_email = admin.email
        except IntegrityError:
            pass
        self.stdout.write(
            self.style.SUCCESS(f'current admin panel user "{admin_email}"')
        )
