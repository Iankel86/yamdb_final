from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Кастомная модель пользователя + роли."""
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLES = [
        (USER, 'user'),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin'),
    ]
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True
    )
    first_name = models.CharField(
        'Имя',
        max_length=50,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=50,
        blank=True
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=150,
        unique=True
    )
    bio = models.TextField(
        'Краткая информация',
        blank=True,
        null=True
    )
    role = models.CharField(
        'Роль',
        max_length=50,
        choices=ROLES,
        default=USER
    )
    confirmation_code = models.CharField(
        'Проверочный код',
        max_length=100,
        unique=True,
        blank=True,
        null=True
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_staff

    class Meta:
        """Метакласс, определяющий поведение класса CustomUser."""
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
