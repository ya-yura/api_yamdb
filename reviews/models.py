from validate import year_validator
from django.db import models


class Category(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name="Наименование категории",
    )

    slug = models.CharField(
        unique=True,
    )


class Genre(models.Model):
    name = models.CharField(
        max_length=128,
        verbose_name="Наименование жанра",
    )

    slug = models.CharField(
        unique=True,
    )


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name="Наименование произведения",
    )

    year = models.CharField(
        default="",
        max_length=4,
        validators=[year_validator],
        verbose_name='Год произведения'
    )

    description = models.CharField(
        max_length=256,
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


class Review(models.Model):
    pass


class Comment(models.Model):
    pass