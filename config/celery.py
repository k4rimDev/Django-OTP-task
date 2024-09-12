from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab

from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True) # For debugging
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'delete-expired-files-every-day': {
        'task': 'dashboard.tasks.delete_expired_files',
        'schedule': crontab(minute='*/10'), # Every 10 min
    },
}
