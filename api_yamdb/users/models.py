from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
import re

from reviews.constants import EMAIL_MAX_LENGTH, ROLE_MAX_LENGTH


def validate_username(value):
    """Проверяет, имя пользователя."""
    if not re.match(r'^[\w.@+-]+\Z', value):
        raise ValidationError(
            'Имя пользователя содержит недопустимые символы.')
    if value.lower() == 'me':
        raise ValidationError('Имя пользователя "me" недопустимо.')


class User(AbstractUser):
    """Модель пользователя с дополнительными полями: email, bio и role."""

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLE_CHOICES = [
        (ADMIN, 'Админ'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь')
    ]
    email = models.EmailField(max_length=EMAIL_MAX_LENGTH, unique=True)
    bio = models.TextField("Биография", blank=True, null=True)
    role = models.CharField(
        "Роль",
        max_length=ROLE_MAX_LENGTH,
        choices=ROLE_CHOICES,
        default=USER
    )
    username = models.CharField(
        "username",
        max_length=150,
        unique=True,
        validators=[validate_username]
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        """Является ли user администратором или суперпользователем."""
        return self.role == self.ADMIN or self.is_staff

    @property
    def is_moderator(self):
        """Проверяет, является ли пользователь модератором."""
        return self.role == self.MODERATOR

    def make_random_password(self):
        """Генерирует случайный пароль для пользователя."""
        return get_random_string()

    def clean(self):
        """Дополнительная проверка значения поля username перед сохранением."""
        super().clean()
        validate_username(self.username)
