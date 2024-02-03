from django.urls import path
from .views import SendCodeView, VerifyPhoneView, LoginView, RegisterView, ResetPasswordView, UserInfo

urlpatterns = [
    path('Register/', RegisterView.as_view(), name='register'),
    path('Login/', LoginView.as_view(), name='login'),
    path('ResetPassword/', SendCodeView.as_view(), name='send-code'),
    path('VerifyPhone/', VerifyPhoneView.as_view(), name='confirm-code'),
    path('VerifyPassword/', ResetPasswordView.as_view(), name='reset-password'),
]
