from django.db import models
from django.contrib.auth import get_user_model
from validate import year_validator
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


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
