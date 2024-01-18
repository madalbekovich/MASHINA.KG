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