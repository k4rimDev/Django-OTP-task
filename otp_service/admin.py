from django.contrib import admin

from otp_service.models import OTP


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'chance_count')
