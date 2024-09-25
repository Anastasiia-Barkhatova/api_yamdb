import re

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.utils import IntegrityError
from django.utils.crypto import get_random_string
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from reviews.constants import (CONFIRMATION_CODE_MAX_LENGTH, EMAIL_MAX_LENGTH,
                               USERNAME_MAX_LENGTH)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя."""

    class Meta:
        model = User
        fields = (
            'username', 'email', 'bio', 'role', 'first_name', 'last_name'
        )


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя."""

    email = serializers.EmailField(max_length=EMAIL_MAX_LENGTH)
    username = serializers.CharField(max_length=USERNAME_MAX_LENGTH)

    def validate_username(self, value):
        """Проверка поля username."""
        if value == 'me':
            raise serializers.ValidationError(
                "Использовать имя 'me' в качестве username запрещено."
            )
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                "Содержание поля username не соответствует паттерну."
            )
        return value

    def create(self, validated_data):
        """Создание нового юзера и отправка кода подтверждения на email."""
        try:
            user, created = User.objects.get_or_create(
                email=validated_data['email'],
                defaults={'username': validated_data['username']}
            )
            if not created:
                user.username = validated_data['username']

            confirmation_code = get_random_string()
            user.set_password(confirmation_code)
            user.save()
            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения: {confirmation_code}',
                settings.EMAIL_HOST_USER,
                [validated_data['email']],
                fail_silently=False,
            )
        except IntegrityError:
            raise ValidationError("A user with this username already exists.")
        return user


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена пользователя."""

    username = serializers.CharField(max_length=USERNAME_MAX_LENGTH)
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_MAX_LENGTH
    )
