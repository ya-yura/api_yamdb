from rest_framework import serializers
from django.db import IntegrityError
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework.validators import UniqueValidator

from reviews.models import Category, Genre, Title, Genre, Review, Comment, User


class RegistrationSerializer(serializers.ModelSerializer):
    """Сериализует запросы на регистрацию."""
    username = serializers.RegexField(
        max_length=settings.LIMIT_USERNAME,
        regex=r'^[\w.@+-]+\Z',
        required=True
    )
    email = serializers.EmailField(
        max_length=settings.LIMIT_EMAIL,
        required=True,
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Использовать имя me запрещено!')
        return value

    class Meta:
        fields = ('username', 'email')
        model = User

    def validate_empty(self, data):
        username = data.get('username')
        email = data.get('email')
        if not username:
            raise serializers.ValidationError(
                'Имя пользователя не может быть пустым'
            )
        if not email:
            raise serializers.ValidationError(
                'Email не может быть пустым'
            )
        return data

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        try:
            user = User.objects.create(username=username, email=email)
        except IntegrityError:
            raise serializers.ValidationError('Это имя или email уже занято')
        return user


class TokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        max_length=settings.LIMIT_USERNAME,
        regex=r'^[\w.@+-]+\Z',
        required=True)
    confirmation_code = serializers.CharField(
        max_length=settings.LIMIT_CODE,
        required=True)

    class Meta:
        fields = ('username', 'confirmation_code')
        model = User


class UserSerializer(serializers.ModelSerializer):
    """Сериализует данные пользователя."""
    username = serializers.RegexField(
        max_length=settings.LIMIT_USERNAME,
        regex=r'^[\w.@+-]+\Z',
        required=True,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ])
    email = serializers.EmailField(
        max_length=settings.LIMIT_EMAIL,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User

    def validate_empty(self, data):
        username = data.get('username')
        email = data.get('email')
        if not username:
            raise serializers.ValidationError(
                'Имя пользователя не может быть пустым'
            )
        if not email:
            raise serializers.ValidationError(
                'Email не может быть пустым'
            )
        return data


class UserEditSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        max_length=settings.LIMIT_USERNAME,
        regex=r'^[\w.@+-]+\Z',
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        max_length=settings.LIMIT_EMAIL,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ])

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Category
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ['id']
        model = Genre
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class TitleCreateSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        allow_null=False
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )
        model = Title


class TitleDisplaySerializer(serializers.ModelSerializer):
    genre = CategorySerializer(many=True)
    category = GenreSerializer()
    rating = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )
        model = Title


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор моделей комментариев."""
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate_score(self, value):
        if 0 > value > 10:
            raise serializers.ValidationError(
                'Оценка по 10-бальной шкале!')
        return value

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=author).exists()
        ):
            raise ValidationError(
                'Больше одного отзыва на title писать нельзя'
            )
        return data
