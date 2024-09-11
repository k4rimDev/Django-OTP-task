from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from otp_service.models import OTPDevice


class GenerateOTPView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        otp_device, created = OTPDevice.objects.get_or_create(user=user)
        otp_device.generate_otp()

        if 'email' in request.data:
            otp_device.send_otp_via_email()
        else:
            otp_device.send_otp_via_sms()

        return Response({'message': 'OTP sent successfully.'})


class VerifyOTPView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        otp_code = request.data.get('otp_code')
        otp_device = OTPDevice.objects.get(user=request.user)

        if otp_device.is_valid_otp(otp_code):
            return Response({'message': 'OTP is valid.'})
        else:
            return Response({'message': 'Invalid OTP or OTP has expired.'}, status=400)
