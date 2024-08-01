from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(value):
    """Валидатор для проверки года"""
    if value > timezone.now().year:
        raise ValidationError(
            'Пожалуйста, введите корректный год!'
        )
