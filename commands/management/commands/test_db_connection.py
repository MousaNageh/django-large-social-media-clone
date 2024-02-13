from django.core.management.base import BaseCommand
from django.db import connections
import time


class Command(BaseCommand):
    help = "wait until db connection is established"

    def handle(self, *args, **options):
        i = 1
        while i < 5:
            try:
                connections["default"].cursor()
                break
            except Exception as e:
                print("database not ready to connect")
                print(e)
                time.sleep(5)
                i += 1

        self.stdout.write(self.style.SUCCESS("data base ready to connect"))
