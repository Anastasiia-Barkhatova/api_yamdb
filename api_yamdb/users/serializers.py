from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'bio', 'role', 'first_name', 'last_name')


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)

    def validate(self, data):
        if data['username'].lower() == 'me':
            raise serializers.ValidationError("Использовать имя 'me' в качестве username запрещено.")
        return data

    def create(self, validated_data):
        user, created = User.objects.get_or_create(
            email=validated_data['email'],
            defaults={'username': validated_data['username']}
        )
        if created:
            confirmation_code = user.make_random_password()
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
