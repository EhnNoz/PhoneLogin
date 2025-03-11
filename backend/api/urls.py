from django.urls import path
from .views import SendVerificationCode, VerifyCode, RefreshTokenView

urlpatterns = [
    path('send-code/', SendVerificationCode.as_view(), name='send-code'),
    path('verify-code/', VerifyCode.as_view(), name='verify-code'),
    # path('refresh-token/', RefreshTokenView.as_view(), name='refresh-token'),

]