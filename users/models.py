import random

from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

class Users(AbstractUser):
    username = None

    phone = models.CharField('Номер телефона', max_length=13, unique=True)

    code = models.IntegerField('код потверждение', null=True)

    activated = models.BooleanField('Активировано', default=False)

    USERNAME_FIELD = 'phone'

    objects = UserManager()

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = ''.join([str(random.randint(0, 9)) for _ in range(4)])
        super(Users, self).save(*args, **kwargs)


class Meta:
    verbose_name = 'ПОЛЬЗОВАТЕЛЬ'
    verbose_plural = 'пользователи'