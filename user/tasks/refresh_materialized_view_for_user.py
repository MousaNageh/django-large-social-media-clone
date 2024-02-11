from celery import shared_task
from django.db import connection

from user.utilities import PG_USER_PER_WEEK_MATERIALIZED_VIEW_NAME


@shared_task(name="refresh_user_statistics_materialized_view_every_week")
def refresh_user_statistics_materialized_view_every_week():
    with connection.cursor() as cursor:
        try:
            cursor.execute(
                f"REFRESH MATERIALIZED VIEW CONCURRENTLY {PG_USER_PER_WEEK_MATERIALIZED_VIEW_NAME}"
            )
            print(
                f"materialized view '{PG_USER_PER_WEEK_MATERIALIZED_VIEW_NAME}' is refreshed successfully"
            )
        except Exception as e:
            print(e)
