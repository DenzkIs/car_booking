import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# celery beat task

app.conf.beat_schedule = {
    # 'request_day_km': {
    #     'task': 'booking.tasks.request_car_day_info',
    #     'schedule': crontab(minute='35', hour='16')
    # },
    'request_and_insert_day_mileage': {
        'task': 'booking.tasks.request_and_insert_day_mileage',
        'schedule': crontab(minute='5', hour='3')
    },
    'add_day_mileage_to_car': {
        'task': 'booking.tasks.add_day_mileage_to_car',
        'schedule': crontab(minute='1', hour='9')
    }
}
