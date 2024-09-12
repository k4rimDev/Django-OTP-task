from celery import shared_task

from django.utils import timezone

from dashboard.models import File


@shared_task
def delete_expired_files():
    """Delete files that have passed their expiration date."""
    now = timezone.now()
    expired_files = File.objects.filter(expiration_date__lt=now)
    count, _ = expired_files.delete()
    return f"{count} expired files deleted."
