import random
import string

from datetime import timedelta

from django.core.mail import send_mail
from django.utils import timezone
from django.core.cache import cache

from otp_service.models import OTP


class OTPService:
    @staticmethod
    def generate_otp(user):
        """Generates a 6-digit OTP for the user and saves it to the OTP model."""
        otp_code = ''.join(random.choices(string.digits, k=6))
        otp_device, created = OTP.objects.get_or_create(user=user)
        otp_device.otp_code = otp_code
        otp_device.otp_created_at = timezone.now()
        otp_device.save()

        return otp_code

    @staticmethod
    def send_otp_via_email(user, otp_code):
        """Sends OTP to the user's email."""
        subject = "Your OTP Code"
        message = f"Your OTP code is {otp_code}. This code is valid for 5 minutes."
        send_mail(subject, message, 'no-reply@myproject.com', [user.email])

    @staticmethod
    def verify_otp(user, code):
        """Verifies if the provided OTP is valid and has not expired."""
        try:
            otp_device = OTP.objects.get(user=user)
            if otp_device.otp_code == code and (timezone.now() - otp_device.otp_created_at) <= timedelta(minutes=5):
                return True
            return False
        except OTP.DoesNotExist:
            return False

    @staticmethod
    def rate_limit_otp(user):
        """Prevents OTP spam by limiting the frequency of OTP generation."""
        if cache.get(f'otp_rate_limit_{user.id}'):
            return True
        cache.set(f'otp_rate_limit_{user.id}', True, timeout=60)  # 1 minute timeout
        return False
