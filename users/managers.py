from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone,  password=None, **spec_fields):
        if not phone:
            raise ValueError('Это поле должно заполнится!')

        user = self.model(phone=phone, **spec_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, phone, password=None, **spec_fields):
        spec_fields.setdefault('is_staff', True)
        spec_fields.setdefault('is_superuser', True)

        if spec_fields.get('is_staff') is not True:
            raise ValueError('Супер пользватель должен иметь True')
        if spec_fields.get('is_superuser') is not True:
            raise ValueError('Супер пользователь должен иметь is_superuser=True')

        return self.create_user(phone, password, **spec_fields)