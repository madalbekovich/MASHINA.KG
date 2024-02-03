from rest_framework import status
from rest_framework.generics import (
    GenericAPIView,
    CreateAPIView,
    RetrieveAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from .servises import send_sms
from .models import Users
from .serializers import (
    RegisterSerializers,
    VerifyPhoneSerializer,
    SendCodeSerializer,
    LoginSerializer,
    UserProfileSerializer,
    ResetPasswordSerializer,
    ResetPasswordVerifySerializer,
)


class RegisterView(CreateAPIView):
    queryset = Users.objects.all()
    serializer_class = RegisterSerializers

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            if user.activated:
                return Response({
                    'response': False,
                    'message': ('Пользватель с таким именем уже активирован!')
                },
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Убираем os_registration
            # user_id = user.id
            # firstname = user.first_name
            # lastname = user.last_name
            # os_registration(user_id, firstname, lastname)

            sms = send_sms(user.phone, "Подтвердите номер телефона", user.code)
            if sms:
                return Response(
                    {
                        "response": True,
                        "message": _("Код подтверждения был отправлен на ваш номер."),
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {"response": False, "message": _("Что то пошло не так!")},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class VerifyPhoneView(GenericAPIView):
    serializer_class = VerifyPhoneSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            code = serializer.data["code"]
            phone = serializer.data["phone"]

            try:
                user = Users.objects.get(phone=phone)

                if user.activated:
                    return Response({"message": _("Аккаунт уже подтвержден")})

                if user.code == code:
                    user.activated = True
                    user.save()

                    return Response(
                        {
                            "response": True,
                            "message": _("Пользователь успешно зарегистрирован."),
                        }
                    )
                return Response(
                    {"response": False, "message": _("Введен неверный код")}
                )
            except ObjectDoesNotExist:
                return Response(
                    {
                        "response": False,
                        "message": _("Пользователь с таким телефоном не существует"),
                    }
                )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class SendCodeView(GenericAPIView):
    serializer_class = SendCodeSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            phone = serializer.data["phone"]

            try:
                user = Users.objects.get(phone=phone)
            except ObjectDoesNotExist:
                return Response(
                    {
                        "response": False,
                        "message": _("Пользователь с таким телефоном не существует"),
                    },
                )
            if not user.activated:
                user.save()

                sms = send_sms(phone, "Ваш новый код подтверждения", user.code)

                return Response({"response": True, "message": _("Код отправлен")})

            return Response(
                {"response": False, "message": _("Аккаунт уже подтвержден")}
            )
        return Response(serializer.errors)


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            phone = request.data.get("phone")
            password = request.data.get("password")

            try:
                get_user = Users.objects.get(phone=f"{''.join(filter(str.isdigit, phone))}")
            except ObjectDoesNotExist:
                return Response(
                    {
                        "response": False,
                        "message": _("Пользователь с указанными телефоном не существует"),
                    }
                )

            user = authenticate(request, phone=f"{''.join(filter(str.isdigit, phone))}", password=password)

            if not user:
                return Response(
                    {
                        "response": False,
                        "message": _("Неверный пароль"),
                    }
                )

            if user.activated:
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "response": True,
                        "message": "",
                        "token": token.key,
                    }
                )
            return Response(
                {
                    "response": False,
                    "message": _("Подтвердите номер, чтобы войти!"),
                    "isactivated": False,
                }
            )

        return Response(serializer.errors)


class UserInfo(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_info = UserProfileSerializer(request.user).data
        return Response(user_info)


class ChangePasswordView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            password = serializer.data["password"]
            confirm_password = serializer.data["confirm_password"]

            if password != confirm_password:
                return Response({"response": False, "message": _("Пароли не совпадают")})

            user.set_password(password)
            user.save()

            return Response({"response": True, "message": _("Пароль успешно обновлен")})
        return Response(serializer.errors)


class ResetPasswordView(GenericAPIView):
    serializer_class = ResetPasswordVerifySerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            phone = serializer.data["phone"]
            try:
                user = Users.objects.get(phone=f"{''.join(filter(str.isdigit, phone))}")
                user.save()

                send_sms(phone, "Подтвердите номер для сброса пароля", user.code)
                return Response({"response": True, "message": _("Код подтверждения был отправлен на ваш номер")})
            except ObjectDoesNotExist:
                return Response({"response": False, "message": _("Пользователь с таким номером не существует")})
        return Response(serializer.errors)


class ResetPasswordVerifyView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            code = serializer.data["code"]
