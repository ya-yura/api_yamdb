from django.db import models
from django.contrib.auth.models import AbstractUser
from api.validators import UsernameValidator, username_not_me
from django.conf import settings


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    ]
    username_validator = UsernameValidator()
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=settings.LIMIT_EMAIL,
        unique=True,)
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=settings.LIMIT_USERNAME,
        null=True,
        unique=True,
        validators=[username_validator, username_not_me],

    )
    bio = models.TextField(
        verbose_name='О себе',
        null=True,
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        choices=ROLES,
        default=USER
    )
