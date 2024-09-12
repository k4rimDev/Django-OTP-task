from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from services.otp_service import OTPService


User = get_user_model()


class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            otp_code = OTPService.generate_otp(user)
            OTPService.send_otp_via_email(user, otp_code)

            return Response({'message': 'OTP sent to your email'})
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=400)


class VerifyLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp_code')
        try:
            user = User.objects.get(email=email)
            if OTPService.verify_otp(user, otp_code):
                return Response({'message': 'OTP verified, login successful'})
            else:
                return Response({'error': 'Invalid OTP'}, status=400)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=400)
