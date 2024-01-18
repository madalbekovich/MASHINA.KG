from django.contrib import admin
from .models import PassengerCars, CarModel, CarBrand

admin.site.register(PassengerCars)
admin.site.register(CarModel)
admin.site.register(CarBrand)


