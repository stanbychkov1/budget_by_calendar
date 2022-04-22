import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'budget_by_calendar.settings')

app = Celery('budget_by_calendar')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
