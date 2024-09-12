from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from dashboard.models import File


class UserProfileView(LoginRequiredMixin, ListView):
    model = File
    template_name = 'auth/profile.html'
    context_object_name = 'files'

    def get_queryset(self):
        return File.objects.filter(owner=self.request.user)
