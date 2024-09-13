from __future__ import absolute_import, unicode_literals

import os
import logging

from celery import Celery
from celery.schedules import crontab

from django.conf import settings


logger = logging.getLogger("Celery")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

app.config_from_object('django.conf:settings')
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


app.conf.update(
    BROKER_URL='redis://:{password}@redis:6379/0'.format(password=os.getenv("REDIS_PASSWORD", None)),
    CELERY_RESULT_BACKEND='redis://:{password}@redis:6379/1'.format(password=os.getenv("REDIS_PASSWORD", None)),
    CELERY_DISABLE_RATE_LIMITS=True,
    CELERY_ACCEPT_CONTENT=['json', ],
    CELERY_TASK_SERIALIZER='json',
    CELERY_RESULT_SERIALIZER='json',
    CELERY_IMPORTS = ('account.tasks', 'dashboard.tasks')
)
