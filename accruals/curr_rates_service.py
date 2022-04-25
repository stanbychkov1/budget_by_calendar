import datetime
import requests

from .models import Rate, Currency

ruble_cur, created = Currency.objects.get_or_create(
        title='руб',
        iso_title='RUR',
        iso_code='810'
    )


def get_rates(last_date, month, day):
    url = f'https://www.cbr-xml-daily.ru/archive/{last_date.year}/{month}/{day}/daily_json.js'
    response = requests.get(
            url=url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
    if response.status_code == 200:
        rates = response.json()
        for rate_x in rates['Valute'].items():
            currency, created = Currency.objects.get_or_create(
                    title=rate_x[1]['CharCode'],
                    iso_title=rate_x[1]['CharCode'],
                    iso_code=rate_x[1]['NumCode']
                )
            rate, created = Rate.objects.get_or_create(
                    currency=currency,
                    rate=str(rate_x[1]['Value']),
                    nominal=rate_x[1]['Nominal'],
                    date=last_date
                )
        ruble_rate, created = Rate.objects.get_or_create(
                    currency=ruble_cur,
                    rate=str(1),
                    nominal=1,
                    date=last_date
                )
    elif response.status_code == 404:
        yesterday = last_date - datetime.timedelta(days=1)
        last_rates = Rate.objects.filter(date=yesterday)
        for rate_x in last_rates:
            rate_x.pk = None
            rate_x.date = last_date
            rate_x.save()
    else:
        pass
