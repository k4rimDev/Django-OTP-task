from datetime import timedelta

from django.db import models
from django.utils import timezone


class OTP(models.Model):
    phone_number = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    chance_count = models.IntegerField(default=4)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    last_sent_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timezone.timedelta(minutes=10)
        if not self.last_sent_at:
            self.last_sent_at = timezone.now()
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at
    
    def can_resend(self):
        return timezone.now() > self.last_sent_at + timezone.timedelta(minutes=1)

    def reset_chance_count(self):
        if self.created_at < timezone.now() - timezone.timedelta(hours=1):
            self.chance_count = 4
            self.save()

    def __str__(self):
        return f'{self.phone_number} - {self.otp_code}'
