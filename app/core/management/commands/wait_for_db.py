from psycopg2 import OperationalError as Psycopg2Error
from django.db import OperationalError
from django.core.management.base import BaseCommand
import time


class Command(BaseCommand):
    help = "Waits for the database to become available."

    def add_arguments(self, parser):
        parser.add_argument('--sleep-interval', type=int, default=1,
                            help='Time to wait between checks, in seconds.')

    def handle(self, *args, **options):
        db_up = False
        attempts = 0
        max_attempts = 30
        while not db_up and attempts < max_attempts:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                time.sleep(1)
                attempts += 1
