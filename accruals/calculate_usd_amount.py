from . import models
from decimal import Decimal as dec

from .curr_rates_service import get_rates


def calculation(currency, amount, date, usd_rate):
    if currency.iso_code == '810':
        amount_USD = dec(amount) / (
                dec(usd_rate.rate) / dec(usd_rate.nominal))
    elif currency.iso_title == 'USD':
        amount_USD = amount
    else:
        currency_rate = models.Rate.objects.get(
            currency__iso_title=currency.iso_title,
            date=date
        )
        usd_rate = models.Rate.objects.get(
            currency__iso_title='USD',
            date=date
        )
        usd_rate_nom = dec(usd_rate.rate) / dec(usd_rate.nominal)
        curr_rate_nom = dec(currency_rate.rate) / dec(
            currency_rate.nominal)
        amount_USD = dec(amount) * curr_rate_nom / usd_rate_nom
    return amount_USD


def calc_usd_amount(currency, amount, date):
    amount_USD = 0
    if not isinstance(currency, models.Currency):
        currency = models.Currency.objects.get(id=currency)
    try:
        usd_rate = models.Rate.objects.get(
            currency__iso_title='USD',
            date=date
        )
        amount_USD = calculation(currency, amount, date, usd_rate)
    except models.Rate.DoesNotExist:
        pass
    except models.Rate.MultipleObjectsReturned:
        query_to_delete = models.Rate.objects.filter(date=date)
        query_to_delete.delete()
        get_rates(last_date=date, url_date=date)
        usd_rate = models.Rate.objects.get(
            currency__iso_title='USD',
            date=date
        )
        amount_USD = calculation(currency, amount, date, usd_rate)
    return amount_USD
