from django.urls import path, include
from .views import SendCodeAPIView, ConfirmCodeAPIView

urlpatterns = [
    path('send-code/', SendCodeAPIView.as_view(), name='send-code'),
    path('confirm-code/', ConfirmCodeAPIView.as_view(), name='confirm-code'),
    path('accounts/', include('allauth.urls')),
]
