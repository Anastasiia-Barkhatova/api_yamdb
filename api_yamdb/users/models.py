from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=[
            ('user', 'User'),
            ('moderator', 'Moderator'),
            ('admin', 'Admin'),
        ],
        default='user'
    )

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == 'moderator'
