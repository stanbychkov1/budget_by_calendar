import os
import datetime

import caldav
from dotenv import load_dotenv

from . import models
from .calculate_usd_amount import calc_usd_amount

load_dotenv()

URL = os.getenv('URL')
USER_NAME = os.getenv('USER_NAME')
PASSWORD = os.getenv('PASSWORD')
CAL_NAME = os.getenv('CAL_NAME')


def uploading_calendar_data(start_date, end_date, user_id):
    error_list = []
    vevents = []

    # Подключение к серверу
    client = caldav.DAVClient(url=URL, username=USER_NAME, password=PASSWORD)
    # Получение индивидуальной ссылки к календарям
    try:
        my_principal = client.principal()
    except OSError as e:
        error_list.append('Отсутствует подключение к интернету')
        return error_list

    # Получение данных из "рабочего" календаря
    events = my_principal.calendar(name=CAL_NAME).date_search(
        start=start_date,
        end=end_date,
        expand=True
    )

    for event in events:
        vevents.extend(event.vobject_instance.contents['vevent'])

    for vevent in vevents:
        try:
            date = datetime.datetime.date(
                vevent.contents['dtstart'][0].value)
        except TypeError:
            date = vevent.contents['dtstart'][0].value
        UUID = vevent.contents['uid'][0].value
        summary = vevent.contents['summary'][0].value
        try:
            currency = models.Currency.objects.get(iso_code='810')
        except models.Currency.DoesNotExist:
            currency = None
        amount_USD = 0
        try:
            patient_name, amount, *rest = summary.split('/')
            # создание Начислений, с проверкой на существование
            # уже загруженных начислений
            if rest:
                # выделяем валюту начисления
                iso_title = rest[0]
                try:
                    currency = models.Currency.objects.get(iso_title=iso_title)
                except models.Currency.DoesNotExist:
                    currency = None

            if currency is not None:
                amount_USD = calc_usd_amount(currency, amount, date)

            if not models.Accrual.objects.filter(uuid=UUID,
                                                 date=date).exists():
                # Нахождение или создание пациента
                patient, created = models.Patient.objects.get_or_create(
                    name=patient_name,
                    user_id=user_id)
                # Создание начисления
                models.Accrual.objects.create(
                    user_id=user_id,
                    patient=patient,
                    date=date,
                    amount=amount,
                    uuid=UUID,
                    info=summary,
                    currency=currency,
                    amount_USD=amount_USD
                )
        except ValueError:
            error_list.append(f'Не загружено событие от {date} c UUID {UUID}'
                              f' и данными {summary}')
            continue
    return error_list
