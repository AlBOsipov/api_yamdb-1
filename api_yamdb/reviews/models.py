from django.db import models

from django.contrib.auth.models import AbstractUser, BaseUserManager
from reviews.services import validate_name_me


ROLE_SET = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class UserManager(BaseUserManager):
    """Новые правила регистрации юзера."""
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_unusable_password()
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
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
