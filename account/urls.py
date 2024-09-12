from django.urls import path
from django.contrib.auth.views import LogoutView

from account.views import (
    UserProfileView,
    OTPLoginView,
    OTPVerifyView
)


urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('logout/', LogoutView.as_view(next_page='file_list'), name='logout'),

    # OTP urls
    path('otp-login/', OTPLoginView.as_view(), name='otp_login'),
    path('verify-otp/', OTPVerifyView.as_view(), name='verify_otp'),
]
