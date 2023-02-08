import re
from django.core.exceptions import ValidationError


def validate_username(value):
    if value == 'me':
        raise ValidationError(
            ('Имя пользователя не может быть <me>.'),
            params={'value': value},
        )
    if re.search(r'^[-a-zA-Z0-9_]+$', value) is None:
        raise ValidationError(
            ('Не допустимые символы '), params={'value': value},)
