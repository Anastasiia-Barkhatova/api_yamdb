from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
import re

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'role', 'first_name', 'last_name')

class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError("Использовать имя 'me' в качестве username запрещено.")
        if not re.match(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError("Содержание поля username не соответствует паттерну.")
        return value

    def create(self, validated_data):
        user, created = User.objects.get_or_create(
            email=validated_data['email'],
            defaults={'username': validated_data['username']}
        )
        if created:
            confirmation_code = get_random_string()
            user.set_password(confirmation_code)
            user.save()
            send_mail(
                'Confirmation code',
                f'Your confirmation code is {confirmation_code}',
                settings.EMAIL_HOST_USER,
                [validated_data['email']],
                fail_silently=False,
            )
        return user

class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(max_length=128)
