from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

from rest_framework import status

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import (UserSerializer,
                          SelfUserPageSerializer, TokenSerializer)
from reviews.models import YaMdbUser


# Эндпоинт /singup/
# Принмиает для поля email и username
# Отправляет confirmation_code на почту
class CreateUserAPIView(APIView):
    """Создание нового пользователя."""
    permission_classes = (AllowAny,)

    def post(self, request):
        """Регистрация нового пользователя."""
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirmation_code = self.generat_conf_code(user)
        self.send_code_on_email(user, confirmation_code)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def generat_conf_code(self, user):
        """Генератор пользовательского кода."""
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()
        return confirmation_code

    def send_code_on_email(self, user, token):
        """Отправка кода подтверждения на почту."""
        header = 'Ваш код подтверждения'
        message = ''.join([
            f'Приветствуем {user.username} путник 10 спринта! \n',
            f'Держи свой код: {token}'
        ])
        mail_from = 'verif@yamdb.ru'
        email = user.email
        try:
            send_mail(header, message, mail_from, [email])
        except Exception as error:
            return (f'Хотели написать но, {error}')


# Эндпоинт /users/me/
class SelfUserPageViewSet(APIView):
    """API для получения информации о собственной странице пользователя."""

    def get(request):
        serializer = SelfUserPageSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Эндпоинт /token/
# Принмиает для поля username и confirmation_code
# Отдает access JWT токен
class TokenView(TokenObtainPairView):
    """Получение токена."""
    serializer_class = TokenSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        code = serializer.validated_data.get('confirmation_code')

        # Проверяем, что оба поля заполнены
        if not username or not code:
            return Response({
                'error': 'username и code должны быть заполнены'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, что пользователь с таким именем существует
        try:
            user = YaMdbUser.objects.get(username=username)
        except YaMdbUser.DoesNotExist:
            return Response({
                'error': 'Пользователь с таким именем не найден'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем, что переданный код подтверждения верен
        if not default_token_generator.check_token(user, code):
            return Response({
                'error': 'Неверный код подтверждения'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Отправляем токен
        try:
            refresh = AccessToken.for_user(user)
            return Response({
                'token': str(refresh),
            })
        except Exception as error:
            return Response({
                'error': f'Неверный код подтверждения {error}'
            }, status=status.HTTP_400_BAD_REQUEST)
