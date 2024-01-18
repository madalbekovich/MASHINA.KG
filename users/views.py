from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, SendCodeSerializer
from .models import Users


class SendCodeAPIView(APIView):
    serializer_class = SendCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone']

        try:
            user = Users.objects.get(phone=phone_number)
        except Users.DoesNotExist:
            # Если пользователь не найден, создаем нового пользователя
            user = Users.objects.create(phone=phone_number)

        if not user.activated:
            # Здесь вызывайте вашу логику отправки кода активации
            user.save() # Замените эту строку на ваш вызов

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
