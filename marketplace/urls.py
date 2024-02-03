from django.urls import path
from .views import *

urlpatterns = [
    path('list/', CarList.as_view()),
    path('detail/<int:pk>/', CarDetail.as_view()),
    path('add/', CarAdd.as_view())
]
