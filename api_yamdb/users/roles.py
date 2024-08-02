from django.db import models


class Roles(models.TextChoices):
    """Определяем перечисление ролей пользователя"""
    USER = 'user', 'пользователь'
    MODERATOR = 'moderator', 'модератор'
    ADMIN = 'admin', 'администратор'
