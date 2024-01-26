from rest_framework import generics
from .models import PassengerCars
from .serializers import PassengerCarsLISTSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


class PassengerCarsList(generics.ListAPIView):
    queryset = PassengerCars.objects.all()
    serializer_class = PassengerCarsLISTSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['mark', 'model', 'manufacturing_year', 'body', 'engine', 'drive', 'gearbox',
                        'wheel', 'modification'
                        ]

