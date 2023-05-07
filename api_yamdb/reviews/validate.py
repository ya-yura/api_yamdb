import datetime
from django.core.exceptions import ValidationError


def year_validator(value):
    if int(value) <= 0 or int(value) > datetime.datetime.now().year:
        raise ValidationError(
            (f'<error> Значение года: {value} указано некорректно!'),
            params={'value': value},
        )
