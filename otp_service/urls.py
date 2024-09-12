from django.urls import path
from otp_service.views import GenerateOTPView, VerifyOTPView


urlpatterns = [
    path('generate-otp/', GenerateOTPView.as_view(), name='generate-otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
]
