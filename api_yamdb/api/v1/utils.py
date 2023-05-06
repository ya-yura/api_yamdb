from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string

from user.models import User


def get_confirmation_code():
    """Генерирует confirmation_code."""
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%&*'
    return get_random_string(20, chars)


def send_confirmation_code(request):
    """Отправляет сгенерированный confirmation_code пользователю."""
    user = get_object_or_404(
        User,
        username=request.data.get('username'),
    )
    user.confirmation_code = get_confirmation_code()
    user.save()
    send_mail(
        'данные для получеия токена',
        f'Код подтверждения {user.confirmation_code}',
        'token@yamdb.ru',
        [request.data.get('email')],
    )
