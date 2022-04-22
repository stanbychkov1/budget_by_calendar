import datetime
# from urllib import request
import requests

from budget_by_calendar.celery import app

from .models import Rate, Currency


@app.task(bind=True, name='uploading_rates')
def upload_rates(self):
    try:
        obj = Rate.objects.latest('date')
    except Rate.DoesNotExist:
        obj = False
    if obj:
        last_date = obj.date + datetime.timedelta(days=1)
    else:
        last_date = datetime.date(2021, 9, 1)
    ruble_cur, created = Currency.objects.get_or_create(
        title='руб',
        iso_title='RUR',
        iso_code='810'
    )
    while last_date <= datetime.date.today():
        month = str(last_date.month).zfill(2)
        day = str(last_date.day).zfill(2)
        url = f'https://www.cbr-xml-daily.ru/archive/{last_date.year}/{month}/{day}/daily_json.js'
        response = requests.get(
            url=url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
            # request.urlopen(url, headers={'User-Agent': 'Mozilla/5.0'})
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
            last_date += datetime.timedelta(days=1)
        elif response.status_code == 404:
            yesterday = last_date - datetime.timedelta(days=1)
            last_rates = Rate.objects.filter(date=yesterday)
            for rate_x in last_rates:
                rate_x.pk = None
                rate_x.date = last_date
                rate_x.save()
            last_date += datetime.timedelta(days=1)
        else:
            continue

    # soup = BS(urlopen(url))
    # dictionary = {'tags': {}}
    # for tag in soup.findAll():
    #     try:
    #         dictionary['tags'][tag.name] += 1
    #     except KeyError:
    #         dictionary['tags'][tag.name] = 1
    # if 'html' in dictionary['tags'].keys():
    #     return dictionary
    # return {'response': 'It is not a html site'}
