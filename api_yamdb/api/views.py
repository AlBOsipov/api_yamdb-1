from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .pagination import UserPagination
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from reviews.models import YaMdbUser
from rest_framework import viewsets
from .serializers import UserSerializer, SelfUserPageSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator


# Эндпоинт /singup/
# Принмиает для поля email и username
# Отправляет confirmation_code на почту
class CreateUserAPIView(APIView):
    """Создание нового пользователя."""
    permission_classes = (AllowAny,)

    def generat_conf_code(self, user):
        """Генератор пользовательского кода."""
        confirmation_code = default_token_generator.make_token(user)
        user.confirmation_code = confirmation_code
        user.save()
        return confirmation_code

    def send_code_on_email(self, generat_conf_code):
        """Отправка кода подтверждения на почту."""
        user = self.user
        token = generat_conf_code(user)
        header = 'Ваш код подтверждения'
        message = (
            f'Приветствуем {user.user_name} путник 10 спринта! \n',
            f'Держи свой код: {token}'
        )
        mail_from = 'verif@yamdb.ru'
        email = user.email
        try:
            send_mail(header, message, mail_from, email)
        except Exception as error:
            f'Хотели написать но, {error}'

    # Валидация username and email проходит на уровене модели
    # надо реализовать фукнцию отправки сообщения
    def post(self, request):
        """Регистрация нового пользователя."""
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

# Эндпоинт /token/
# Принмиает для поля username и confirmation_code
# Отдает access JWT токен
class AuthUserAPIView(APIView):
    """Кастомная форма авторизации."""
    # Пока не помню как сделать на эндпоинте обязательные к запросу поля.
    # Моя логика:
    # Просим обязательные поля
    # проводим их валидацию
    def validate_date(self, request):
        username = request.get('username')
        confirmation_code = request.get('confirmation_code')

    # этой фукнцией мы генерим JWT токен
    def get_tokens_for_user(self, request):
        """Запрос своего JWT токена."""
        user = request
        refresh = RefreshToken.for_user(user)
        return {'access': str(refresh.access_token)}


class SelfUserPageViewSet(viewsets.ModelViewSet):
    """Получение данных о себе."""
    serializer_class = SelfUserPageSerializer

    def get_queryset(self):
        return self.kwargs["username"]
