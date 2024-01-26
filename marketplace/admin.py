from django.contrib import admin
from .models import *


class PassengerCarsDescAdmin(admin.StackedInline):
    model = PassengersCarsDesc
    extra = 1
    min_num = 1
    max_num = 1

    fieldsets = (
        ('Основные параметры', {
            'fields': (
                'state', 'mileage')
        }),
        ('Внешний вид', {
            'fields': (
            'obves', 'tinted_windows', 'spoiler', 'alloy_wheels', 'sunroof', 'winch', 'roof_rails',
            'roof_rack', 'tow_hitch', 'panoramic_roof'),
        }),
        ('Салон', {
            'fields': (
                'velour_upholstery', 'leather_upholstery', 'window_shades', 'alcantara_upholstery',
                'combination_upholstery',
                'wood_trim'
            ),
        }),
        ('Медиа', {
            'fields': (
                'cd_player', 'dvd_player', 'mp3_player', 'usb_port', 'subwoofer'
            )
        }),
        ('Безопасность', {
            'fields': (
                'abs', 'traction_control', 'stability_control', 'airbags', 'parking_sensors', 'rearview_camera',
            ),
        }),
        ('Опция', {
            'fields': (
                'full_power_package', 'alarm_system', 'factory_auto_start', 'air_conditioning', 'climate_control',
                'lpg_conversion', 'cruise_control', 'heated_front_seats', 'heated_seats', 'heated_mirrors',
                'xenon_headlights', 'bi_xenon_headlights', 'headlight_washers', 'air_suspension', 'memory_seats',
                'memory_steering_wheel', 'rain_sensor', 'light_sensor', 'advertisements_text'
            )
        })


    )


class PassengerCarsImgInline(admin.TabularInline):
    model = PassengerCarsImg
    extra = 0


class PassengerCarsVideoInline(admin.TabularInline):
    model = PassengerCarsVideo
    extra = 1


class PriceCarAdmin(admin.StackedInline):
    model = PriceCar
    extra = 1
    min_num = 1
    max_num = 1


class AddInfoCarAdmin(admin.StackedInline):
    model = AddInfoCar
    extra = 1
    min_num = 1
    max_num = 1


class GovernNumberCarsAdmin(admin.StackedInline):
    model = GovernNumberCars
    extra = 1
    min_num = 1
    max_num = 1


class ContactsCarsAdmin(admin.StackedInline):
    model = ContactsCars
    extra = 1
    min_num = 1
    max_num = 1


class GovernNumberCarAdmin(admin.StackedInline):
    model = GovernNumberCars
    extra = 1
    min_num = 1
    max_num = 1


@admin.register(PassengerCars)
class PassengerCarsIMGAdmin(admin.ModelAdmin):
    inlines = [
        PassengerCarsImgInline,
        PassengerCarsVideoInline,
        PassengerCarsDescAdmin,
        AddInfoCarAdmin,
        GovernNumberCarAdmin,
        PriceCarAdmin,
        ContactsCarsAdmin,
        # PassengerCarsDescAdmin,
        # ContactsCarsAdmin,


    ]
    list_display = ['id', 'mark', 'model', 'manufacturing_year']



admin.site.register(CarRegion)
admin.site.register(CarArea)
admin.site.register(CarBrand)
admin.site.register(CarModel)