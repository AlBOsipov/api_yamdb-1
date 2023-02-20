from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer, SelfUserPageSerializer, TokenSerializer

from rest_framework_simplejwt.tokens import AccessToken

from django.contrib.auth import authenticate



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
            print(f'Хотели написать но, {error}')


# Эндпоинт /users/me/
class SelfUserPageViewSet(APIView):
    """API для получения информации о собственной странице пользователя."""

    def get(request):
        serializer = SelfUserPageSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
# Эндпоинт /token/
# Принмиает для поля username и confirmation_code
# Отдает access JWT токен
class TokenView(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            code = serializer.validated_data['confirmation_code']
            user = authenticate(request, username=username, confirmation_code=code)
            if user:
                refresh = AccessToken.for_user(user)
                return Response({'token': str(refresh)}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

