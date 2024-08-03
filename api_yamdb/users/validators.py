from django.core.exceptions import ValidationError


def validate_username_me(value):
    """Проверяем, является ли имя пользователя зарезервированным."""

    reserved_username = 'me'
    if value.casefold() == reserved_username:
        raise ValidationError(
            f'Имя "{value}" зарезервировано и не может быть использовано')
