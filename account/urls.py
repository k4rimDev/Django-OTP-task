from django.urls import path
from django.contrib.auth.views import LogoutView

from account.views import UserProfileView


urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('logout/', LogoutView.as_view(next_page='file_list'), name='logout'),
]
