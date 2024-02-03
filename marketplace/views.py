from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PassengerCars
from .serializers import PassengerCarsLISTSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django_filters import rest_framework as all_filter


class CarListFilter(all_filter.FilterSet):
    class Meta:
        model = PassengerCars
        fields = ['mark', 'model', 'manufacturing_year', 'body', 'engine', 'drive', 'gearbox', 'wheel', 'modification']


class CarList(generics.ListAPIView):
    queryset = PassengerCars.objects.all().order_by('-id')
    serializer_class = PassengerCarsLISTSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CarListFilter


class CarDetail(generics.RetrieveAPIView):
    queryset = PassengerCars.objects.all()
    serializer_class = PassengerCarsLISTSerializer


class CarAdd(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PassengerCarsLISTSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)