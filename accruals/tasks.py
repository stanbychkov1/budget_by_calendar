import datetime

from budget_by_calendar.celery import app
from .curr_rates_service import get_rates

from .models import Rate


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
    while last_date <= datetime.date.today():
        month = str(last_date.month).zfill(2)
        day = str(last_date.day).zfill(2)
        get_rates(last_date, month, day)
        last_date += datetime.timedelta(days=1)

