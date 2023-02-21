from reviews.models import Review, Title, Genre, Category
from rest_framework import viewsets, permissions
from api.serializers import (ReviewSerializer, CommentSerializer,
                             TitleSerialzier, GenreSerializer,
                             CategorySerializer)
from django.shortcuts import get_object_or_404

from rest_framework.permissions import (IsAuthenticatedOrReadOnly,
                                        IsAuthenticated)

from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

from rest_framework import status, filters
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import (UserSerializer, UserSingUpSerializer,
                          SelfUserPageSerializer, TokenSerializer)
from reviews.models import YaMdbUser
from .permissions import AdminPermission


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с моделями произведений"""

    serializer_class = TitleSerialzier
    queryset = Title.objects.all()
    # permission_classes = (IsAuthenticatedOrReadOnly, )


class GenreViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с моделями жанров"""

    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    # permission_classes = (IsAuthenticatedOrReadOnly, )


class CategoriesViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с моделями категорий"""

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, AdminPermission)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с моделями отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        '''Функция возвращения всех комментариев поста.'''
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        '''Функция создания нового комментария к посту.'''
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        serializer.save(author=self.request.user,
                        title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с моделями комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        '''Функция возвращения всех комментариев поста.'''
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(
            Review.objects.filter(title_id=title.id),
            pk=review_id
        )
        return review.comments.all()

    def perform_create(self, serializer):
        '''Функция создания нового комментария к посту.'''
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, pk=title_id)
        review_id = self.kwargs.get("review_id")
        review = get_object_or_404(
            Review.objects.filter(title_id=title.id),
            pk=review_id
        )
        serializer.save(author=self.request.user,
                        review=review)


# Эндпоинт /singup/
# Принмиает поля email и username
# Отправляет confirmation_code на почту
class CreateUserAPIView(APIView):
    """Создание нового пользователя."""
    permission_classes = (AllowAny,)

    def post(self, request):
        """Регистрация нового пользователя."""
        # Проверяем есть ли пользователь, True отдает код.

        # Cоздаем пользователя, генерим код и отправляем email.
        user = request.data
        serializer = UserSingUpSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirmation_code = self.generat_conf_code(user)
        self.send_code_on_email(user, confirmation_code)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

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
            }, status=status.HTTP_404_NOT_FOUND)

        # Проверяем, что пользователь с таким именем существует
        try:
            user = YaMdbUser.objects.get(username=username)
        except YaMdbUser.DoesNotExist:
            return Response({
                'error': 'Пользователь с таким именем не найден'
            }, status=status.HTTP_404_NOT_FOUND)

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


# Эндпоинт /users/
class UserViewSet(viewsets.ModelViewSet):
    queryset = YaMdbUser.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAuthenticated, AdminPermission)

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        if not request.user.is_superuser and request.user.role != 'admin':
            return Response(
                {"message": "У вас нет прав для выполнения этой операции."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_superuser and request.user.role != 'admin':
            return Response(
                {"message": "У вас нет прав для выполнения этой операции."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)

    # Эндпоинт /me
    @action(
        detail=False,
        permission_classes=(permissions.IsAuthenticated,),
        methods=('GET', 'PATCH'),
        url_path='me',
        serializer_class=SelfUserPageSerializer
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PATCH':
            serializer = SelfUserPageSerializer(
                user, data=request.data, partial=True)

            # добавляем проверку на автора или админа
            if not request.user.is_superuser and request.user != user:
                return Response(
                    {"message": "У вас нет прав для этой операции."},
                    status=status.HTTP_403_FORBIDDEN
                )

            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
