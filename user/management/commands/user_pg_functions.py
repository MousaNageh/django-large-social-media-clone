import pycountry
from django.core.management.base import BaseCommand
from django.db import connection

from user.utilities import PG_CREATE_PARTITION_FUNCTION, ACTIVITY_TABLE_NAME


class Command(BaseCommand):
    help = "create  postgres function to automatically create user activity table partitions"

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute(self._user_activity_partition_sql())

    @staticmethod
    def _user_activity_partition_sql():
        country_codes = [country.alpha_2 for country in pycountry.countries]
        create_partitions = ""
        for code in country_codes:
            create_partitions += f"SELECT {PG_CREATE_PARTITION_FUNCTION}('{code}');"
        return f"""
        CREATE OR REPLACE FUNCTION {PG_CREATE_PARTITION_FUNCTION}(p_country_code VARCHAR(2))
        RETURNS VOID AS $$
        DECLARE
            partition_name TEXT;
        BEGIN
            partition_name := 'user_activities_' || p_country_code;
            IF partition_name = 'user_activities_' THEN partition_name := 'user_activities_default'; END IF;
            IF NOT EXISTS(SELECT 1 FROM pg_class WHERE relname = partition_name) THEN
                EXECUTE FORMAT('CREATE TABLE %I PARTITION OF {ACTIVITY_TABLE_NAME} FOR VALUES IN (%L)', 
                partition_name, p_country_code);
            END IF;
            RETURN;
        END;
        $$ LANGUAGE plpgsql;
        {create_partitions}
        """
