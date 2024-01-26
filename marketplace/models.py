from django.contrib.auth import get_user_model
from django.db import models
from .choices import *
from smart_selects.db_fields import ChainedForeignKey
from django.core.validators import MinValueValidator, MaxValueValidator


class CarBrand(models.Model):
    name = models.CharField('Brand', max_length=50)

    def __str__(self):
        return self.name


class CarModel(models.Model):
    mark = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    model = models.CharField(max_length=50, verbose_name='Модель')

    def __str__(self):
        return self.model


class PassengerCars(models.Model):
    mark = models.ForeignKey(CarBrand, on_delete=models.CASCADE)
    model = ChainedForeignKey(
        CarModel,
        chained_field='mark',
        chained_model_field='mark',
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.CASCADE
    )
    manufacturing_year = models.IntegerField()
    body = models.CharField(max_length=50, choices=TYPE_BODY, verbose_name='Тип кузова')
    generation = models.ImageField(upload_to='media/', verbose_name='Поколение')
    engine = models.CharField(max_length=50, choices=FUEL, verbose_name='Двигатель')
    drive = models.CharField(max_length=50, choices=DRIVE, verbose_name='Привод')
    gearbox = models.CharField(max_length=50, choices=GEARBOX, verbose_name='Каробка передач')
    wheel = models.CharField(choices=STEERING_WHEEL, verbose_name='Руль', max_length=400)
    modification = models.CharField(max_length=255, verbose_name='Модификация')
    video_youtube = models.URLField(max_length=200, help_text='Введите URL-ссылку на YouTube видео',
                                    verbose_name='Видео')

    def __str__(self):
        return f"{self.mark} {self.model}"

    class Meta:
        verbose_name = 'Добавить объявление'
        verbose_name_plural = 'Добавить объявление'


class PassengerCarsImg(models.Model):
    car = models.ForeignKey(PassengerCars, related_name='img', on_delete=models.CASCADE)
    img = models.ImageField(upload_to='cars/%Y_%m', verbose_name='Фотографии')

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'


class PassengerCarsVideo(models.Model):
    car = models.ForeignKey(PassengerCars, related_name='video', on_delete=models.CASCADE)
    video_youtube = models.URLField(max_length=200, help_text='Введите URL-ссылку на YouTube видео',
                                    verbose_name='Видео')

    class Meta:
        verbose_name = 'Видео'
        verbose_name_plural = 'Видеоролики'


class PassengersCarsDesc(models.Model):
    car = models.ForeignKey(PassengerCars, on_delete=models.CASCADE)
    state = models.CharField('Состояние', max_length=50, choices=STATE)
    mileage = models.BigIntegerField('Пробег', validators=[MinValueValidator(0), MaxValueValidator(999999)])
    obves = models.BooleanField('Обвес', default=False)
    tinted_windows = models.BooleanField('Тонировка', default=False)
    spoiler = models.BooleanField('Спойлер', default=False)
    alloy_wheels = models.BooleanField('Литые диски', default=False)
    sunroof = models.BooleanField('Люк', default=False)
    winch = models.BooleanField('Лебёдка', default=False)
    roof_rails = models.BooleanField('Рейлинги', default=False)
    roof_rack = models.BooleanField('Багажник', default=False)
    tow_hitch = models.BooleanField('Фаркоп', default=False)
    panoramic_roof = models.BooleanField('Панорамная крыша', default=False)
    velour_upholstery = models.BooleanField('Велюр', default=False)
    leather_upholstery = models.BooleanField('Кожа', default=False)
    window_shades = models.BooleanField('Шторки', default=False)
    alcantara_upholstery = models.BooleanField('Алькантара', default=False)
    combination_upholstery = models.BooleanField('Комбинированный', default=False)
    wood_trim = models.BooleanField('Дерево', default=False)
    cd_player = models.BooleanField('CD Player', default=False)
    dvd_player = models.BooleanField('DVD Player', default=False)
    mp3_player = models.BooleanField('MP3 Player', default=False)
    usb_port = models.BooleanField('USB Port', default=False)
    subwoofer = models.BooleanField('Сабвуфер', default=False)
    abs = models.BooleanField('ABS', default=False)
    traction_control = models.BooleanField('Антипробуксовочная система', default=False)
    stability_control = models.BooleanField('Система курсовой устойчивости', default=False)
    airbags = models.BooleanField('Подушки безопасности', default=False)
    parking_sensors = models.BooleanField('Парктроник', default=False)
    rearview_camera = models.BooleanField('Камера заднего вида', default=False)
    full_power_package = models.BooleanField('Полный электропакет', default=False)
    alarm_system = models.BooleanField('Сигнализация', default=False)
    factory_auto_start = models.BooleanField('Автозавод', default=False)
    air_conditioning = models.BooleanField('Кондиционер', default=False)
    climate_control = models.BooleanField('Климат контроль', default=False)
    lpg_conversion = models.BooleanField('Газобалонное оборудование', default=False)
    cruise_control = models.BooleanField('Круиз-контроль', default=False)
    heated_front_seats = models.BooleanField('Подогрев передних сидений', default=False)
    heated_seats = models.BooleanField('Подогрев всех сидений', default=False)
    heated_mirrors = models.BooleanField('Обогрев зеркал', default=False)
    xenon_headlights = models.BooleanField('Ксенон', default=False)
    bi_xenon_headlights = models.BooleanField('Биксенон', default=False)
    headlight_washers = models.BooleanField('Омыватель фар', default=False)
    air_suspension = models.BooleanField('Пневмоподвеска', default=False)
    memory_seats = models.BooleanField('Память сидений', default=False)
    memory_steering_wheel = models.BooleanField('Память руля', default=False)
    rain_sensor = models.BooleanField('Датчик дождя', default=False)
    light_sensor = models.BooleanField('Датчик света', default=False)
    advertisements_text = models.TextField('Текст объявление', max_length=255)

    class Meta:
        verbose_name = 'Комплектация и описание'
        verbose_name_plural = 'Комплектация и описания'


class AddInfoCar(models.Model):
    car = models.ForeignKey(PassengerCars, on_delete=models.CASCADE)
    availability = models.CharField('В наличии', max_length=50, choices=AVAILABILITY, default='В наличии')
    custom_auto = models.CharField('Расстаможен', max_length=100, choices=CUSTOM_AUTO, default='да')
    accounting = models.CharField('Учет', max_length=50, choices=CAR_REGIS_LOCATION_CHOICES, default='Кыргызстан')

    # other = models.CharField('Прочее', max_length=50, choices=)

    class Meta:
        verbose_name = 'Дополнительная информация'
        verbose_name_plural = 'Дополнительная информация'


class GovernNumberCars(models.Model):
    car = models.ForeignKey(PassengerCars, on_delete=models.CASCADE)
    body_number = models.CharField('VIN/ Номер кузова', max_length=17)
    govern_number = models.CharField('Гос номер авто', max_length=10)

    class Meta:
        verbose_name = 'Госномерa и VIN / номер кузова'
        verbose_name_plural = 'Госномер и VIN / номер кузова'


class PriceCar(models.Model):
    car = models.ForeignKey(PassengerCars, on_delete=models.CASCADE)
    # price = models.CharField('Цена', )
    price = models.DecimalField(
        max_digits=10,  # Максимальное количество цифр в числе
        decimal_places=2,  # Количество знаков после запятой
        verbose_name='Цена'
    )
    deal_conditions = models.CharField(
        'Условия сделки',
        max_length=10,
        choices=DEAL_CONDITIONS_CHOICES,
        default='soms',
    )
    exchange_option = models.CharField('Возможность обмена', max_length=50, choices=EXCHANGE_OPTION,
                                       default='рассмотрю варианты')

    class Meta:
        verbose_name = 'Цена и условия сделки'
        verbose_name_plural = 'Цена и условия сделкa'


class CarRegion(models.Model):
    region = models.CharField('регион', max_length=50)

    def __str__(self):
        return self.region


class CarArea(models.Model):
    region = models.ForeignKey(CarRegion, on_delete=models.CASCADE)
    area = models.CharField('регион', max_length=50)

    def __str__(self):
        return self.area


class ContactsCars(models.Model):
    car = models.ForeignKey(PassengerCars, on_delete=models.CASCADE)
    region = models.ForeignKey(CarRegion, on_delete=models.CASCADE)
    area = ChainedForeignKey(
        CarArea,
        chained_field='region',
        chained_model_field='region',
        show_all=False,
        auto_choose=True,
        sort=True,
        on_delete=models.CASCADE
    )
    user_number = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='ContactsCar',
        verbose_name='Номер телефона',
    )

    user_phone_number = models.CharField('Добавить номер', max_length=20)

    def save(self, *args, **kwargs):
        phone_number = self.user_number.phone

        self.user_phone_number = phone_number
        super().save(*args, **kwargs)
