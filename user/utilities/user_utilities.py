from django.contrib.gis.geos import Point
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

USER_REGISTER_SYSTEM_TYPE = "system"
USER_REGISTER_FACEBOOK_TYPE = "facebook"
USER_REGISTER_GOOGLE_TYPE = "google"

USER_REGISTER_TYPE_OPTIONS = [
    (USER_REGISTER_SYSTEM_TYPE, USER_REGISTER_SYSTEM_TYPE),
    (USER_REGISTER_FACEBOOK_TYPE, USER_REGISTER_FACEBOOK_TYPE),
    (USER_REGISTER_GOOGLE_TYPE, USER_REGISTER_GOOGLE_TYPE),
]


USER_MALE_GENDER = "Male"
USER_FEMALE_GENDER = "Female"

USER_GENDER_CHOICES = [
    (USER_MALE_GENDER, USER_MALE_GENDER),
    (USER_FEMALE_GENDER, USER_FEMALE_GENDER),
]
OPT_EXPIRE_TIME_IN_MINUTES = 10
USER_OPT_DURATION = timedelta(minutes=OPT_EXPIRE_TIME_IN_MINUTES)

PG_CREATE_PARTITION_FUNCTION = "user_activity_create_partition_if_not_exists"
ACTIVITY_TABLE_NAME = "user_activities"
USER_TABLE_NAME = "users"

PG_USER_PER_WEEK_MATERIALIZED_VIEW_NAME = "user_per_week_m_view"

DEFAULT_EMAIL_DOMAIN = "@socialclone.com"


def get_point_from_coordinates(lng, lat):
    return Point(lng, lat, srid=4326)


def is_email(input_str):
    validator = EmailValidator()
    try:
        validator(input_str)
        return True
    except ValidationError:
        return False
