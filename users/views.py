from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    UserSerializer,
    SendCodeSerializer,
    LoginSerializer,
    RegistrationSerializer,
    SendCodePasswordSerializer,
    ResetPasswordSerializer,
    UserProfileSerializer


)
from .models import *
from django.contrib.auth import authenticate, login

class SendCodeAPIView(APIView):
    serializer_class = SendCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone']

        try:
            user = Users.objects.get(phone=phone_number)
        except Users.DoesNotExist:
            user = Users.objects.create(phone=phone_number)

        if not user.activated:
            # логика код активации
            user.save()

            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {'detail': 'Пользователь уже активирован.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class ConfirmCodeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        entered_code = request.data.get('code')
        phone_number = request.data.get('phone')

        try:
            user = Users.objects.get(phone=phone_number, code=entered_code)
        except Users.DoesNotExist:
            return Response({'detail': 'Неверный активационный код.'}, status=status.HTTP_400_BAD_REQUEST)

        user.activated = True
        user.save()

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegistrationAPIView(CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()

            phone = serializer.data["phone"]
            user = Users.objects.get(phone=phone)

            return Response(
                {
                    "response": True,
                    "message": ("User successfully registered."),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone = serializer.validated_data['phone']
        entered_password = serializer.validated_data['password']

        try:
            user = Users.objects.get(phone=phone)
        except Users.DoesNotExist:
            return Response({'detail': 'Пользователь не найден.'}, status=status.HTTP_400_BAD_REQUEST)

        if user.check_password(entered_password):
            if user.activated:
                login(request, user)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Пользователь не активирован.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Неверный пароль.'}, status=status.HTTP_400_BAD_REQUEST)

class SendCodePasswordAPIView(APIView):
    serializer_class = SendCodePasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['data']

        try:
            user = Users.objects.get(phone=phone_number)
        except Users.DoesNotExist:
            user = Users.objects.create(phone=phone_number)

        if not user.activated:
            user.save()

            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Пользватель уже активирован'}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordAPIView(APIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail': 'Пароль успешно сброшен'}, status=status.HTTP_200_OK)


class UserProfileAPIView(RetrieveAPIView):
    queryset = Users.objects.all()
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user