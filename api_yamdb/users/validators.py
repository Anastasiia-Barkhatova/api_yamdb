import re

from django.core.exceptions import ValidationError


def validate_username(value):
    """Проверяет, имя пользователя."""
    if not re.match(r'^[\w.@+-]+\Z', value):
        raise ValidationError(
            'Имя пользователя содержит недопустимые символы.')
    if value == 'me':
        raise ValidationError('Имя пользователя "me" недопустимо.')
