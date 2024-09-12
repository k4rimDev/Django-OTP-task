from django import forms


class OTPLoginForm(forms.Form):
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        phone_number = cleaned_data.get('phone_number')

        if not email and not phone_number:
            raise forms.ValidationError("You must provide either an email or phone number.")
        return cleaned_data


class OTPVerifyForm(forms.Form):
    otp = forms.CharField(required=True)
