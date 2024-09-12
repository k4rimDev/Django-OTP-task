import random
import string

from datetime import timedelta

from django.db import models
from django.conf import settings
from django.utils import timezone


class OTPDevice(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    otp_created_at = models.DateTimeField(auto_now_add=True)
    otp_attempts = models.IntegerField(default=4)

    def generate_otp(self):
        self.otp_code = ''.join(random.choices(string.digits, k=6))
        self.otp_created_at = timezone.now()
        self.save()

    def is_valid_otp(self, code):
        if self.otp_code == code and (timezone.now() - self.otp_created_at) <= timedelta(minutes=5):
            return True
        return False

    def reset_otp(self):
        """Reset OTP and attempts."""
        self.otp_code = None
        self.otp_attempts = 4
        self.save()

    def __str__(self):
        return f'OTP for {self.user.email} (created at {self.otp_created_at})'
