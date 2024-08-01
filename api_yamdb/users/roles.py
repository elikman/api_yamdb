from django.db import models


class RoleEnum(models.TextChoices):
    """Определяем перечисление ролей пользователя"""
    USER = 'user', 'User'
    MODERATOR = 'moderator', 'Moderator'
    ADMIN = 'admin', 'Admin'
