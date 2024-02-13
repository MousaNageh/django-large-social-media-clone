from django.core.management.base import BaseCommand
from django.db import connection

from user.utilities import PG_USER_PER_WEEK_MATERIALIZED_VIEW_NAME, USER_TABLE_NAME


class Command(BaseCommand):
    help = "user statistic number of users ber week materialized view"

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            try:
                cursor.execute(self._create_index_and_materialized_view_sql())
                self.stdout.write(
                    self.style.SUCCESS(
                        f"'{PG_USER_PER_WEEK_MATERIALIZED_VIEW_NAME}' "
                        f"MATERIALIZED_VIEW created successfully"
                    )
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(str(e)))
                raise e

    @classmethod
    def _create_index_and_materialized_view_sql(cls):
        return f"""
            DO $$
            BEGIN
               IF NOT EXISTS (SELECT FROM pg_matviews WHERE  matviewname = '{PG_USER_PER_WEEK_MATERIALIZED_VIEW_NAME}')
                THEN
                    EXECUTE '{cls._user_statistics_materialized_views_sql()}';
                END IF;
                IF NOT EXISTS (
                    SELECT 1 FROM pg_class c
                    JOIN   pg_namespace n ON n.oid = c.relnamespace
                    WHERE  c.relname = 'user_per_week_m_view_id_idx'
                ) THEN
                    EXECUTE '{cls._create_index_from_materialized_view_sql()}';
                END IF;
            END
            $$;
        """

    @staticmethod
    def _user_statistics_materialized_views_sql():
        return f"""
                CREATE MATERIALIZED VIEW {PG_USER_PER_WEEK_MATERIALIZED_VIEW_NAME} AS (
                    SELECT
                        ROW_NUMBER() OVER() AS id,
                        week::DATE,
                        SUM(country_week_count)::INTEGER AS user_number,
                        jsonb_agg(jsonb_build_object(country_code, country_week_count)) AS counties
                    FROM (
                        SELECT 
                            country_code,
                            DATE_TRUNC(''WEEK'', created_at) AS week,
                            count(*) AS country_week_count
                        FROM {USER_TABLE_NAME}
                        GROUP BY country_code, week
                    ) AS country_week_table
                    GROUP BY week 
                    ORDER BY week
                );
            """

    @staticmethod
    def _create_index_from_materialized_view_sql():
        return f"CREATE UNIQUE INDEX user_per_week_m_view_id_idx ON {PG_USER_PER_WEEK_MATERIALIZED_VIEW_NAME}(id);"
