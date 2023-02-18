from django.db import models
from django.core.validators import (MinValueValidator, MaxValueValidator, 
                                    RegexValidator)
from reviews.services import validate_name_me

from django.contrib.auth.models import AbstractUser


ROLE_SET = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


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
    year = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(
        # тут вопрос: правильно ли тут писать on_delete=models.CASCADE?
        Category, on_delete=models.CASCADE, related_name='titles'
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name="titles"
    )

    class Meta:
        # Тут не совсем понял, как фильтровать по slug у категории и жанра
        ordering = ('-name', '-year', 'category', 'genre',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


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

