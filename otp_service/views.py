from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import OTPService
from django.contrib.auth import get_user_model


User = get_user_model()


class GenerateOTPView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        otp_code = OTPService.generate_otp(user)
        
        if 'email' in request.data:
            OTPService.send_otp_via_email(user, otp_code)
        else:
            OTPService.send_otp_via_sms(user, otp_code)

        return Response({'message': 'OTP sent successfully.'})


class VerifyOTPView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        otp_code = request.data.get('otp_code')
        user = request.user

        if OTPService.verify_otp(user, otp_code):
            return Response({'message': 'OTP is valid.'})
        else:
            return Response({'message': 'Invalid OTP or OTP has expired.'}, status=400)
