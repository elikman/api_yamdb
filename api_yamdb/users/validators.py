from django.core.exceptions import ValidationError


def validate_username_me(value):
    """Определяем функцию валидации имени пользователя"""
    if value.lower() == 'me':
        raise ValidationError(f'Имя "{value}" использовать нельзя')
