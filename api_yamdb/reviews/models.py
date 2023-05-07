from django.db import models
from django.contrib.auth.models import AbstractUser
from api.validators import UsernameValidator, username_not_me
from django.conf import settings
from reviews.validate import year_validator
from django.core.validators import MaxValueValidator, MinValueValidator


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


class Category(models.Model):
    """Модель категорий произведений."""
    name = models.CharField(
        max_length=128,
        verbose_name="Наименование категории",
    )

    slug = models.SlugField(
        unique=True,
    )

    class Meta:
        ordering = ('name', 'slug')
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра произведений."""
    name = models.CharField(
        max_length=128,
        verbose_name="Наименование жанра",
    )

    slug = models.SlugField(
        unique=True,
    )

    class Meta:
        ordering = ('name', 'slug')
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name="Наименование произведения",
    )

    year = models.PositiveSmallIntegerField(
        default="",
        validators=[year_validator],
        verbose_name='Год произведения'
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание произведения'
    )

    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр произведения',
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        verbose_name='Категория произведения'
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Оценка',
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('author', 'title')

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
