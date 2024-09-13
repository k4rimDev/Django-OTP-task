from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.views.generic import ListView, FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

from account.forms import OTPVerifyForm, OTPLoginForm

from dashboard.models import File

from services.otp_service import OTPService


User = get_user_model()


class UserProfileView(LoginRequiredMixin, ListView):
    model = File
    template_name = 'auth/profile.html'
    context_object_name = 'files'

    def get_queryset(self):
        return File.objects.filter(owner=self.request.user)


class OTPLoginView(FormView):
    template_name = 'auth/otp_login.html'
    form_class = OTPLoginForm
    success_url = reverse_lazy('verify_otp')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        phone_number = form.cleaned_data.get('phone_number')

        user = None
        if email:
            user, created = User.objects.get_or_create(email=email)
            if created:
                user.first_name = email
                user.save()
        elif phone_number:
            user = User.objects.filter(phone_number=phone_number).first()

        if user:
            otp = OTPService.generate_otp(user)
            if email:
                OTPService.send_otp_via_email(user, otp)
            elif phone_number:
                OTPService.send_otp_via_sms(user, otp)

            self.request.session['otp'] = otp
            self.request.session['user_id'] = user.id
            return super().form_valid(form)
        form.add_error(None, "User not found with provided email or phone number")
        return self.form_invalid(form)


class OTPVerifyView(FormView):
    template_name = 'auth/otp_verify.html'
    form_class = OTPVerifyForm
    success_url = reverse_lazy('file_list')

    def form_valid(self, form):
        otp_input = form.cleaned_data.get('otp')
        otp_stored = self.request.session.get('otp')
        user_id = self.request.session.get('user_id')

        if otp_input == str(otp_stored):
            user = User.objects.get(id=user_id)
            login(self.request, user)
            return super().form_valid(form)
        
        form.add_error('otp', 'Invalid OTP code')
        return self.form_invalid(form)
