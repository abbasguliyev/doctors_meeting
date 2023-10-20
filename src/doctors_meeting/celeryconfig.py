from __future__ import absolute_import

import os
from celery import Celery
from django.conf import settings
from doctors_meeting.settings import BASE_DIR
from celery.schedules import crontab
from pathlib import Path
import environ

env = environ.Env(DEBUG=(bool, False))

environ.Env.read_env(os.path.join(BASE_DIR, '../.env'))


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doctors_meeting.settings')


backend = env('CELERY_BACKEND')
broker = env('CELERY_BROKER')

app = Celery('doctors_meeting', backend=backend, broker=broker)
app.conf.broker_url = broker

app.config_from_object('django.conf:settings')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send_appointment_reminder_task": {
        "task": "send_appointment_reminder_task",
        "schedule": crontab(hour=14, minute=30),
    },
    "send_appointment_file_downloaded_reminder_task": {
        "task": "send_appointment_file_downloaded_reminder_task",
        "schedule": crontab(hour=14, minute=30),
    },
}