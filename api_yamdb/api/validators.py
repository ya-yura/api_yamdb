from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError


class UsernameValidator(UnicodeUsernameValidator):
    """Валидация имени пользователя."""
    regex = r'^[\w.@+-]+\z'


def username_not_me(value):
    """Запрет использовать имя me."""
    if value.lower() == 'me':
        raise ValidationError('Имя пользователя me запрещено.')
    return value
