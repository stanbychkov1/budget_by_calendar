import datetime
import requests

from .models import Rate, Currency

URL = 'https://www.cbr-xml-daily.ru'
HEADERS = {'User-Agent': 'Mozilla/5.0'}


def create_rates(response, date):
    """
        Добавление ежеденевных курсов валют в БД.
    """

    # Создание валюты рубль
    ruble_cur, created = Currency.objects.get_or_create(
        title='руб',
        iso_title='RUR',
        iso_code='810'
    )

    rates = response.json()
    for rate_x in rates['Valute'].items():
        currency, created = Currency.objects.get_or_create(
            title=rate_x[1]['CharCode'],
            iso_title=rate_x[1]['CharCode'],
            iso_code=rate_x[1]['NumCode']
        )
        _, created = Rate.objects.get_or_create(
            currency=currency,
            rate=str(rate_x[1]['Value']),
            nominal=rate_x[1]['Nominal'],
            date=date
        )
    _, created = Rate.objects.get_or_create(
        currency=ruble_cur,
        rate=str(1),
        nominal=1,
        date=date
    )


def get_rates(last_date, url_date):
    """
        Функция, которая получает курсы валют и добавляет их в базу.
    """

    url = (f'{URL}/archive/{url_date.year}/{url_date.month:02d}/'
           f'{url_date.day:02d}/daily_json.js')

    # Получения курсов валют на сегодня от API CBR XML RU
    # response = requests.get(
    #     url=url,
    #     headers=HEADERS
    # )
    #
    # # Обработка ответа в соответствии со статусом ответа от сервера
    # if response.status_code == 200:
    #     create_rates(response, last_date)
    # elif response.status_code == 404:
    #     url_date = url_date - datetime.timedelta(days=1)
    #     get_rates(last_date=last_date, url_date=url_date)
    # else:
    #     pass
    #
    response = requests.get(
            url=url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
    ruble_cur, created = Currency.objects.get_or_create(
        title='руб',
        iso_title='RUR',
        iso_code='810'
    )
    match response.status_code:
        case 200:
            rates = response.json()
            for rate_x in rates['Valute'].items():
                currency, created = Currency.objects.get_or_create(
                        title=rate_x[1]['CharCode'],
                        iso_title=rate_x[1]['CharCode'],
                        iso_code=rate_x[1]['NumCode']
                    )
                _, created = Rate.objects.get_or_create(
                        currency=currency,
                        rate=str(rate_x[1]['Value']),
                        nominal=rate_x[1]['Nominal'],
                        date=last_date
                    )
            _, created = Rate.objects.get_or_create(
                        currency=ruble_cur,
                        rate=str(1),
                        nominal=1,
                        date=last_date
                    )
        case 404:
            yesterday = last_date - datetime.timedelta(days=1)
            last_rates = Rate.objects.filter(date=yesterday)
            for rate_x in last_rates:
                rate_x.pk = None
                rate_x.date = last_date
                rate_x.save()
