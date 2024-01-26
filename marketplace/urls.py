from django.urls import path
from .views import PassengerCarsList

urlpatterns = [
    path('detail/', PassengerCarsList.as_view())
]
