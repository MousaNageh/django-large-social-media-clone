from django.core.management.base import BaseCommand
from django.db import connection

from user.utilities import PG_CREATE_PARTITION_FUNCTION, ACTIVITY_TABLE_NAME, PG_USER_PER_WEEK_MATERIALIZED_VIEW_NAME


class Command(BaseCommand):
    help = "user statistic number of users ber week materialized view"

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(self._user_statistics_materialized_views_sql())

    @staticmethod
    def _user_statistics_materialized_views_sql():
        return f"""
            DROP MATERIALIZED VIEW IF EXISTS {PG_USER_PER_WEEK_MATERIALIZED_VIEW_NAME};
            CREATE MATERIALIZED VIEW {PG_USER_PER_WEEK_MATERIALIZED_VIEW_NAME} AS (
                SELECT
                    ROW_NUMBER() OVER() AS id,
                    week::DATE,
                    SUM(country_week_count)::INTEGER AS user_number,
                    json_agg(json_build_object(country_code, country_week_count)) AS counties
                FROM (
                    SELECT 
                        country_code,
                        DATE_TRUNC('WEEK', created_at) AS week,
                        count(*) AS country_week_count
                    FROM users
                    GROUP BY country_code, week
                ) AS country_week_table
                GROUP BY week 
                ORDER BY week
            );
        """
