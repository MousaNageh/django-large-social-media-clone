import random
from django.core.management.base import BaseCommand
from user.utilities import (
    USER_MALE_GENDER,
    USER_FEMALE_GENDER,
    get_point_from_coordinates,
)
from datetime import datetime, timedelta
from faker import Faker
from user.models import User
import string


class Command(BaseCommand):
    help = "create fake users"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument(
            "--users", type=int, help="The number of fake users to create"
        )

    def handle(self, *args, **options):
        users = []
        number_of_users = options.get("users")
        created_user = 0
        for _ in range(number_of_users):
            user = self._get_user()
            if len(users) % 500 == 0:
                try:
                    User.objects.bulk_create(users, batch_size=500)
                    created_user += len(users)
                    self.stdout.write(
                        self.style.SUCCESS(
                            f"created users number: {created_user} users"
                        )
                    )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(str(e)))
                users = []
            users.append(user)
        if users:
            try:
                User.objects.bulk_create(users, batch_size=500)
                created_user += len(users)
                self.stdout.write(
                    self.style.SUCCESS(f"created users number: {created_user} users")
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(str(e)))

    def _get_user(self):
        record = self._get_user_record()
        user = User(**record)
        return user

    @classmethod
    def _get_user_record(cls):
        start_date = datetime(1970, 1, 1)
        end_date = datetime(2010, 12, 31)
        time_between_dates = end_date - start_date
        days_between_dates = time_between_dates.days
        random_number_of_days = random.randrange(days_between_dates)
        random_date = start_date + timedelta(days=random_number_of_days)
        fake = Faker()
        mail_list = fake.email().split("@")
        email = f"{mail_list[0]}-{cls.get_random_string()}@{mail_list[1]}"
        return {
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "gender": random.choice([USER_MALE_GENDER, USER_FEMALE_GENDER]),
            "country_code": random.choice(["US", "EG", "UE", "GB"]),
            "dob": random_date.strftime("%Y-%m-%d"),
            "bio": fake.text(),
            "email": email,
            "username": fake.user_name() + "-" + cls.get_random_string(),
            "coordinates": get_point_from_coordinates(
                float(fake.longitude()), float(fake.latitude())
            ),
            "password": "pbkdf2_sha256$720000$OlwTSBko80eBCQ2TzrRhDS$d0UgAP/oNCJpvSxYVhTD6mf0sW5RvN8e0SZqVcIbCJo=",  # password 12345
            "is_active": True,
        }

    @staticmethod
    def get_random_string():
        return "".join(random.choice(string.ascii_letters) for i in range(5))
