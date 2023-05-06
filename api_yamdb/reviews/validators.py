from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_year(value):
    """Проверка года на будущее время."""
    current_year = timezone.now().year
    if value > current_year:
        raise ValidationError(
            'Марти, ты опять взял Делориан без спроса?!',
        )
    return value
