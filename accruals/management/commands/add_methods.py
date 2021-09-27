import csv

from django.core.management import BaseCommand

from accruals import models


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
                'accruals_method.csv',
                encoding='utf-8',
        ) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                method = models.Method(id=row[0], name=row[1], user_id=row[2])
                method.save()
