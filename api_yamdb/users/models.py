from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=[('user', 'User'), ('moderator', 'Moderator'), ('admin', 'Admin')],
                            default='user')

    def __str__(self):
        return self.username
