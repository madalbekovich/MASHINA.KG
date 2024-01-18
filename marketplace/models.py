from django.db import models
from .choices import *
from smart_selects.db_fields import ChainedForeignKey
from django.core.validators import MinValueValidator, MaxValueValidator



class CarBrand(models.Model):
    name = models.CharField(max_length=50, verbose_name='Brand')

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
    some_field = models.CharField(max_length=50)
    location = models.CharField(max_length=50, choices=LOCATION_CHOICES, verbose_name='Где находится',)
    manufacturing_year = models.IntegerField(
        verbose_name='Дата выпуска',
        validators=[
            MinValueValidator(1960, 'Выберите даьу',),
            MaxValueValidator(datetime.now().year, 'выуаыка')
        ],
        choices=YEAR_CHOICES
    )
    body = models.CharField(max_length=50, choices=TYPE_BODY, verbose_name='Тип кузова')
    generation = models.ImageField(upload_to='mediad/', verbose_name='Поколение')
    engine = models.CharField(max_length=50, choices=FUEL, verbose_name='Двигатель')
    drive = models.CharField(max_length=50, choices=DRIVE, verbose_name='Привод')
    gearbox = models.CharField(max_length=50, choices=GEARBOX, verbose_name='Каробка передач')
    modification = models.IntegerField(choices=STEERING_WHEEL, verbose_name='Руль')
    images = models.ImageField(upload_to='medida/', verbose_name='Фотографии')
    video_youtube = models.URLField(max_length=200, help_text='Введите URL-ссылку на YouTube видео')

    def __str__(self):
        return f"{self.mark} {self.model} ({self.some_field})"

    class Meta:
        verbose_name = 'Добавить объявление'
        verbose_name_plural = 'Добавить объявление'
