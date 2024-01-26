from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import Users


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'


class SendCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('phone',)


class ConfirmCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('code', )

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'username', 'phone', 'code', 'activated']


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['phone', 'password']
    phone = serializers.CharField(min_length=12)
    password = serializers.CharField(write_only=True)


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True, min_length=8)
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone = serializers.CharField(
        required=True,
        min_length=12,
        error_messages={"min_length": "Введите правильный номер"},
    )

    class Meta:
        model = Users
        fields = ["phone", "first_name", "last_name", "password", "confirm_password"]

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        attrs["phone"] = f"{''.join(filter(str.isdigit, attrs.get('phone')))}"

        validate_password(password)

        if password != confirm_password:
            raise serializers.ValidationError("Пароли не совпадают!")

        if Users.objects.filter(phone=attrs.get("phone")).exists():
            raise serializers.ValidationError("Такой номер уже существует!")

        return attrs

    def save(self, **kwargs):
        phone = self.validated_data["phone"]
        first_name = self.validated_data["first_name"]
        last_name = self.validated_data["last_name"]
        password = self.validated_data["password"]

        user = Users(
            phone=phone,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()
        return user


class SendCodePasswordSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(min_length=12)


class ResetPasswordSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(min_length=12)
    code = serializers.CharField(max_length=4)
    new_password = serializers.CharField(min_length=8)
    confirm_password = serializers.CharField(min_length=8)

    class Meta:
        model = get_user_model()
        fields = ['phone', 'code', 'new_password', 'confirm_password']

    def validate(self, data):
        phone = data.get('phone')
        code = data.get('code')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        try:
            user = get_user_model().objects.get(phone=phone, code=code)
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError('Пользователь не найден.')

        if new_password != confirm_password:
            raise serializers.ValidationError('Пароли не совпадают')

        return data

    def save(self):
        phone = self.validated_data['phone']
        new_password = self.validated_data['new_password']
        user = get_user_model().objects.get(phone=phone)
        user.set_password(new_password)
        user.save()