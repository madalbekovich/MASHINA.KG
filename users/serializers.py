from django.core.cache import cache
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import Users


class RegisterSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    phone = serializers.CharField(
        required=True,
        min_length=15,
        error_messages={"min_length": "Введите правильный номер"},
    )

    class Meta:
        model = Users
        fields = ["phone", "password", "confirm_password"]

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        attrs["phone"] = f"{''.join(filter(str.isdigit, attrs.get('phone')))}"

        validate_password(password)

        if password != confirm_password:
            raise serializers.ValidationError("Пароли не совпадают!")

        if Users.objects.filter(phone=attrs.get("phone")).exists():
            raise serializers.ValidationError("Такой номер уже существует!")

        try:
            existing_user = Users.objects.get(phone=attrs.get("phone"))
            if existing_user.activated:
                raise serializers.ValidationError("Пользователь с таким номером уже активирован!")

            # Проверяем, прошло ли уже 15 минут с момента последней отправки кода
            cache_key = f"activation_code_{existing_user.phone}"

            # Получаем время последней отправки кода из кэша
            last_sent_time = cache.get(cache_key)

            # Если время не установлено или прошло более 15 минут, продолжаем выполнение
            if not last_sent_time or (timezone.now() - last_sent_time).total_seconds() > 900:
                # Устанавливаем текущее время в качестве времени последней отправки кода
                cache.set(cache_key, timezone.now(), 900)  # 900 секунд = 15 минут
            else:
                raise serializers.ValidationError("Пожалуйста, подождите перед повторной отправкой кода.")
        except Users.DoesNotExist:
            pass  # Do nothing if the user doesn't exist

        return attrs

    def save(self, **kwargs):
        phone = self.validated_data["phone"]
        password = self.validated_data["password"]

        user = Users(
            phone=phone,
        )
        user.set_password(password)
        user.save()
        return user


class VerifyPhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(
        required=True,
    )
    code = serializers.IntegerField(
        required=True
    )

    class Meta:
        fields = ["phone", "code"]

    def validate(self, attrs):
        attrs["phone"] = f"{''.join(filter(str.isdigit, attrs.get('phone')))}"
        return super().validate(attrs)


class SendCodeSerializer(serializers.Serializer):
    phone = serializers.CharField()

    class Meta:
        fields = ["phone"]

    def validate(self, attrs):
        return super().validate(attrs)


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(
        write_only=True,
        required=True,
    )
    password = serializers.CharField(
        write_only=True,
        # min_length=8,
        required=True,
        # error_messages={"min_length": "Не менее 8 символов."},
    )
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        attrs['phone'] = f"{''.join(filter(str.isdigit, attrs.get('phone')))}"
        return super().validate(attrs)

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        required=True,
        min_length=8,
        error_messages={"min_length": "Не менее 8 символов.", "required": "Это поле обязательно."}
    )
    confirm_password = serializers.CharField(
        required=True,
        min_length=8,
        error_messages={"min_length": "Не менее 8 символов.", "required": "Это поле обязательно."}
    )


class ResetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(
        required=True,
        error_messages={"required": "Это поле обязательно."}
    )

    class Meta:
        fields = ["phone"]

    def validate(self, attrs):
        return super().validate(attrs)


class ResetPasswordVerifySerializer(serializers.Serializer):
    phone = serializers.CharField()
    code = serializers.IntegerField(
        required=True,
        error_messages={"required": "Это поле обязательно."}
    )

    class Meta:
        fields = ["phone", "code"]

    def validate(self, attrs):
        return super().validate(attrs)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'phone', 'code', 'activated']