from django.core.management.base import BaseCommand
from django.db import connection

from user.utilities import PG_CREATE_PARTITION_FUNCTION, ACTIVITY_TABLE_NAME


class Command(BaseCommand):
    help = "create fake users"

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(self._user_activity_partition_sql())

    @staticmethod
    def _user_activity_partition_sql():
        return f"""
        CREATE OR REPLACE FUNCTION {PG_CREATE_PARTITION_FUNCTION}(p_country_code VARCHAR(2))
        RETURNS VOID AS $$
        DECLARE
            partition_name TEXT;
        BEGIN
            partition_name := 'user_activity_' || p_country_code;
            IF NOT EXISTS(SELECT 1 FROM pg_class WHERE relname = partition_name) THEN
                EXECUTE FORMAT('CREATE TABLE %I PARTITION OF {ACTIVITY_TABLE_NAME} FOR VALUES IN (%L)', 
                partition_name, p_country_code);
            END IF;
            RETURN;
        END;
        $$ LANGUAGE plpgsql;
        """
