from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from reviews.models import User
from django.conf import settings


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
