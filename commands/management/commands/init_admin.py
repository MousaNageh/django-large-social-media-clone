from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand
from django.utils.timezone import now
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
                country_code='EG',
                coordinates=Point(31.235712, 30.044420),
                username=admin_email,
                gender=USER_MALE_GENDER,
                last_login=now()
            )
            admin_email = admin.email

        except Exception as E:
            self.stdout.write(
                self.style.ERROR(f'{str(E)}')
            )
            return
        self.stdout.write(
            self.style.SUCCESS(f'current admin panel user "{admin_email}"')
        )
