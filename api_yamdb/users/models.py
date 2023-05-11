from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from api.validators import UsernameValidator, username_not_me


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator'),
        (USER, 'user'),
    ]
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=settings.LIMIT_EMAIL,
        unique=True,)
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=settings.LIMIT_USERNAME,
        null=True,
        unique=True,
        validators=[UsernameValidator(), username_not_me],
    )
    first_name = models.CharField('Имя',
                                  max_length=settings.LIMIT_USERNAME,
                                  blank=True)
    last_name = models.CharField('Фамилия',
                                 max_length=settings.LIMIT_USERNAME,
                                 blank=True)
    bio = models.TextField(
        verbose_name='О себе',
        null=True,
        blank=True
    )
    role = models.CharField(
        verbose_name='Роль',
        max_length=settings.LIMIT_ROLE,
        choices=ROLES,
        default=USER
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.is_superuser or self.role == self.ADMIN

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
