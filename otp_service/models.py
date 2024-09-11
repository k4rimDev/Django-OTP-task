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

    def generate_otp(self):
        self.otp_code = ''.join(random.choices(string.digits, k=6))
        self.otp_created_at = timezone.now()
        self.save()

    def is_valid_otp(self, code):
        if self.otp_code == code and (timezone.now() - self.otp_created_at) <= timedelta(minutes=5):
            return True
        return False

    def send_otp_via_email(self):
        subject = "Your OTP Code"
        message = f"Your OTP code is {self.otp_code}. This code is valid for 5 minutes."
        self.user.email_user(subject, message)

    def send_otp_via_sms(self):
        print(f"Sending OTP {self.otp_code} to {self.user.phone_number}")
