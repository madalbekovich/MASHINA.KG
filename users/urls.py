from django.urls import path, include
from .views import SendCodeAPIView, ConfirmCodeAPIView, LoginAPIView, RegistrationAPIView, ResetPasswordAPIView, \
    UserProfileAPIView

urlpatterns = [
    path('send-code/', SendCodeAPIView.as_view(), name='send-code'),
    path('confirm-code/', ConfirmCodeAPIView.as_view(), name='confirm-code'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegistrationAPIView.as_view(), name='register'),
    path('reset-password', ResetPasswordAPIView.as_view(), name='reset-password'),
]
