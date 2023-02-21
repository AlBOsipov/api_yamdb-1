from django.db import models
from django.core.validators import (
    MinValueValidator, MaxValueValidator, RegexValidator
)
import datetime
from reviews.services import validate_name_me
from django.contrib.auth.models import AbstractUser, BaseUserManager


ROLE_SET = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class UserManager(BaseUserManager):
    """Новые правила регистрации юзера."""
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(('Пароль обязателен.'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class YaMdbUser(AbstractUser):
    """Переопределенная модель пользователя."""
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[validate_name_me]
    )
    email = models.EmailField(
        'E-mail',
        max_length=254,
        unique=True
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Уровень доступа',
        max_length=15,
        choices=ROLE_SET,
        default='user',
    )
    password = None
    confirmation_code = models.CharField(
        'Код подтвержедния',
        max_length=50,
        null=True,
        blank=False,
        default=None
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    object = UserManager()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Category(models.Model):
    """Модель категорий"""

    name = models.CharField(max_length=256, verbose_name="Название")
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(regex=r'^[-a-zA-Z0-9_]+$',
                    message='Некорректный slug.')]
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанров"""

    name = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(regex=r'^[-a-zA-Z0-9_]+$',
                    message='Некорректный slug.')]
    )

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений"""

    name = models.CharField(max_length=256)
    year = models.IntegerField(
        validators=[MinValueValidator(0),
                    MaxValueValidator(datetime.datetime.now().year)]
    )
    description = models.TextField()
    category = models.ForeignKey(
        Category, null=True, on_delete=models.SET_NULL, related_name='titles'
    )
    genres = models.ManyToManyField(Genre, through='GenreTitle')

    class Meta:
        # ordering = ('name', 'year', 'category', 'genres',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель для связи многим ко многим произведения и жанра"""
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'

    class Meta:
        verbose_name = 'Жанр-произведение'
        verbose_name_plural = 'Жанры-произведения'


class Review(models.Model):
    """Модель для отзывов к произведениям."""

    author = models.ForeignKey(
        YaMdbUser, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель для комментариев к отзывам."""

    author = models.ForeignKey(
        YaMdbUser, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
