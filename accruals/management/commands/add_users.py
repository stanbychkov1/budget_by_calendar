import csv
from datetime import datetime

from django.core.management import BaseCommand

from accruals import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
                'auth_user.csv',
                encoding='utf-8',
        ) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                user = models.User(id=row[0],
                                   password=row[1],
                                   # last_login=(row[2]),
                                   is_superuser=row[3],
                                   username=row[4],
                                   # last_name=row[5],
                                   # email=row[6],
                                   is_staff=row[7],
                                   is_active=row[8],
                                   # date_joined=row[9],
                                   # first_name=row[10],
                                   )
                user.save()
