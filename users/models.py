from django.contrib.auth.models import AbstractUser
from django.db import models

from django_otp.models import OTPDevice


class User(AbstractUser):
    otp_device = models.OneToOneField(OTPDevice, on_delete=models.SET_NULL, null=True, blank=True)
    email_verified = models.BooleanField(default=False)

    def generate_otp(self):
        pass
