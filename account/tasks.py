from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings

from celery import shared_task


@shared_task
def send_email_task(subject: str, body: str, to_mail: str):
    message = EmailMessage(subject=subject, body=body, from_email = f"<{settings.EMAIL_HOST_USER}>", to=[to_mail, ])
    message.content_subtype = 'html'
    message.send()
