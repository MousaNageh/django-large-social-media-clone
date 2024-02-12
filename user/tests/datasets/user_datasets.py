from datetime import datetime, timedelta
from faker import Faker
import random

from user.utilities import (
    get_point_from_coordinates,
    USER_MALE_GENDER,
    USER_FEMALE_GENDER,
)


def get_user_object(is_active=True):
    start_date = datetime(1970, 1, 1)
    end_date = datetime(2010, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    fake = Faker()
    return {
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "gender": random.choice([USER_MALE_GENDER, USER_FEMALE_GENDER]),
        "country_code": random.choice(["US", "EG", "AF", "GB", "DZ", "AD"]),
        "dob": random_date.strftime("%Y-%m-%d"),
        "bio": fake.text(),
        "email": fake.email(),
        "username": fake.user_name(),
        "coordinates": get_point_from_coordinates(
            float(fake.longitude()), float(fake.latitude())
        ),
        "password": fake.password(length=10, special_chars=True),
        "is_active": is_active,
    }



