from rest_framework import serializers
from .models import (
    CarBrand,
    CarModel,
    PassengerCars,
    PassengerCarsImg,
    PassengerCarsVideo,
    AddInfoCar,
    GovernNumberCars,
    PassengersCarsDesc,
    PriceCar,
    ContactsCars
)


class CarBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarBrand
        fields = ('id', 'name')


class CarModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarModel
        fields = ('id', 'mark', 'model')


class PassengerCarsImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengerCarsImg
        fields = ('id', 'img')


class PassengerCarsVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengerCarsVideo
        fields = ('id', 'video_youtube')


class GovernNumberCarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GovernNumberCars
        fields = ('body_number', 'govern_number')


class AddInfoCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddInfoCar
        fields = ('availability', 'custom_auto', 'accounting')


class PassengerCarsDescSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengersCarsDesc
        fields = '__all__'


class PriceCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceCar
        fields = '__all__'


class ContactsCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactsCars
        fields = '__all__'


class PassengerCarsLISTSerializer(serializers.ModelSerializer):
    mark = CarBrandSerializer()
    model = CarModelSerializer()
    images = PassengerCarsImgSerializer(many=True, read_only=True)
    videos = PassengerCarsVideoSerializer(many=True, read_only=True)
    govern_number = GovernNumberCarsSerializer(source='governnumbercars_set', many=True)
    add_info = AddInfoCarSerializer(source='addinfocar_set', many=True)
    passengers_cars_desc = PassengerCarsDescSerializer(source='passengerscarsdesc_set', many=True)
    price_car = PriceCarSerializer(source='pricecar_set', many=True)
    contacts_cars = ContactsCarSerializer(source='contactscars_set', many=True)

    class Meta:
        model = PassengerCars
        fields = (
            'id', 'mark', 'model', 'manufacturing_year', 'body', 'engine', 'drive', 'gearbox', 'wheel',
            'modification', 'images', 'videos', 'govern_number', 'add_info', 'passengers_cars_desc',
            'price_car', 'contacts_cars'
        )
