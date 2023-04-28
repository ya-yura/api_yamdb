from validate import year_validator
from django.db import models


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
        max_length=4,
        validators=[year_validator],
        verbose_name='Год произведения'
    )

    description = models.CharField(
        blank=True,
        null=True,
        verbose_name='Описание произведения'
    )

    genre = models.ManyToManyField(
        Genre,
        through='Genre',
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
        ordering = ('name', 'year', 'genre', 'category')
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    pass


class Comment(models.Model):
    pass