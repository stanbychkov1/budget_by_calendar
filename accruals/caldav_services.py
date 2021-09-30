import os
import datetime

import caldav
from dotenv import load_dotenv

from . import models

load_dotenv()


URL = os.getenv('URL')
USER_NAME = os.getenv('USER_NAME')
PASSWORD = os.getenv('PASSWORD')
CAL_NAME = os.getenv('CAL_NAME')


def uploading_calendar_data(start_date, end_date, user_id):
    # Подключение к серверу
    client = caldav.DAVClient(url=URL, username=USER_NAME, password=PASSWORD)
    # Получение индивидуальной ссылки к календарям
    my_principal = client.principal()
    # Получение данных из "рабочего" календаря
    events = my_principal.calendar(name=CAL_NAME).date_search(
        start=start_date,
        end=end_date,
        expand=True)
    error_list = []
    for event in events:
        # Получаемую строку события изменяем в словарь
        event_dict = {}
        for elem in event.data.split('\n')[:-1]:
            if ':' not in elem:
                elem += ':'
            new_elem = elem.split(':')
            event_dict[new_elem[0]] = new_elem[1]
        # Выделяются данные для создания модели
        date = datetime.datetime.strptime(
            event_dict['DTSTART;TZID=Europe/Moscow'], '%Y%m%dT%H%M%S')
        UUID = event_dict['UID']
        summary = event_dict['SUMMARY']
        try:
            patient_name, amount, *_ = summary.split('/')
            # создание Начислений, с проверкой на существование
            # уже загруженных начислений
            if not models.Accrual.objects.filter(uuid__exact=UUID).exists():
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
                    info=event_dict['SUMMARY']
                )
        except ValueError:
            error_list.append(f'Не загружено событие от {date} c UUID {UUID}'
                              f' и данными {summary}')
            continue
    return error_list
