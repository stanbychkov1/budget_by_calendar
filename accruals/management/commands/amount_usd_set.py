from django.core.management import BaseCommand

from accruals import models
from accruals.calculate_usd_amount import calc_usd_amount

mods = (models.Accrual, models.Payment,)


class Command(BaseCommand):
    def handle(self, *args, **options):
        for mod in mods:
            non_cur_models = mod.objects.filter(amount_USD=0)
            for model in non_cur_models:
                model.currency = models.Currency.objects.get(iso_code='810')
                model.amount_USD = calc_usd_amount(
                    model.currency, model.amount, model.date)
                model.save()
