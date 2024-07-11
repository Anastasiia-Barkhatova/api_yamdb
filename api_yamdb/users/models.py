from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.crypto import get_random_string

from reviews.constants import EMAIL_FIELD_MAX_LENGTH, ROLE_MAX_LENGTH


class User(AbstractUser):
    """Модель пользователя с дополнительными полями: email, bio и role."""

    email = models.EmailField(max_length=EMAIL_FIELD_MAX_LENGTH, unique=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(
        max_length=ROLE_MAX_LENGTH,
        choices=[
            ('user', 'User'),
            ('moderator', 'Moderator'),
            ('admin', 'Admin'),
        ],
        default='user'
    )

    @property
    def is_admin(self):
        """
        Проверяет, является ли пользователь администратором.

        или суперпользователем.
        """
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        """Проверяет, является ли пользователь модератором."""
        return self.role == 'moderator'

    def make_random_password(self):
        """Генерирует случайный пароль для пользователя."""
        return get_random_string()
