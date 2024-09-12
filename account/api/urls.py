from django.urls import path

from account.api.views import LoginView, VerifyLoginView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('verify-login/', VerifyLoginView.as_view(), name='verify-login'),
]
