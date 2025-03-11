from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import PhoneNumberSerializer, VerificationCodeSerializer
import random
from rest_framework_simplejwt.tokens import RefreshToken


# class SendVerificationCode(APIView):
#     def post(self, request):
#         serializer = PhoneNumberSerializer(data=request.data)
#         if serializer.is_valid():
#             phone_number = serializer.validated_data['phone_number']
#             user, created = User.objects.get_or_create(phone_number=phone_number)
#             verification_code = str(random.randint(100000, 999999))
#             print(verification_code)
#             user.verification_code = verification_code
#             user.save()
#             # در اینجا کد تأیید را به شماره تلفن کاربر ارسال کنید (مثلاً با استفاده از سرویس SMS)
#             return Response({'message': 'Verification code sent'}, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# if send_sms(phone_number, message):
#     return Response({'message': 'Verification code sent'}, status=status.HTTP_200_OK)
# else:
#     return Response({'message': 'Failed to send verification code'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SendVerificationCode(APIView):
    def post(self, request):
        serializer = PhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            user, created = User.objects.get_or_create(phone_number=phone_number)
            verification_code = str(random.randint(100000, 999999))
            print(verification_code)
            user.set_verification_code(verification_code)  # تنظیم کد تأیید و زمان انقضای آن
            # در اینجا کد تأیید را به شماره تلفن کاربر ارسال کنید (مثلاً با استفاده از سرویس SMS)
            return Response({'message': 'Verification code sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class VerifyCode(APIView):
#     def post(self, request):
#         serializer = VerificationCodeSerializer(data=request.data)
#         if serializer.is_valid():
#             phone_number = serializer.validated_data['phone_number']
#             verification_code = serializer.validated_data['verification_code']
#             try:
#                 user = User.objects.get(phone_number=phone_number, verification_code=verification_code)
#                 user.is_verified = True
#                 user.save()
#                 return Response({'message': 'User verified successfully'}, status=status.HTTP_200_OK)
#             except User.DoesNotExist:
#                 return Response({'message': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCode(APIView):
    def post(self, request):
        serializer = VerificationCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = serializer.validated_data['verification_code']
            try:
                user = User.objects.get(phone_number=phone_number, verification_code=verification_code)
                # بررسی انقضای کد تأیید
                if user.verification_code_expiry and user.verification_code_expiry >= timezone.now():
                    user.is_verified = True
                    # user.verification_code = None  # پاک کردن کد تأیید پس از استفاده
                    # user.verification_code_expiry = None  # پاک کردن زمان انقضای کد تأیید
                    user.save()

                    # ایجاد توکن‌های JWT
                    # refresh = RefreshToken.for_user(user)
                    # access_token = str(refresh.access_token)
                    # refresh_token = str(refresh)
                    # return Response({
                    #     'message': 'User verified successfully',
                    #     'access_token': access_token,
                    #     'refresh_token': refresh_token,
                    # }, status=status.HTTP_200_OK)
                    print(user.password)
                    return Response({'message': 'User verified successfully','password': user.password}, status=status.HTTP_200_OK)
                else:
                    user.is_verified = False
                    user.verification_code = None
                    user.verification_code_expiry = None

                    return Response({'message': 'Verification code has expired'}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({'message': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(APIView):
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'message': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({
                'access_token': access_token,
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)