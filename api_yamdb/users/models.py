from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.constants import (
    CONST_EMAIL_LENGTH,
    CONST_ROLE_LENGTH,
    CONST_CONFIRMATION_LENGTH,
    CONST_USERNAME_LENGTH,
)
from users.roles import Roles
from users.validators import validate_username_me


class CinemaUser(AbstractUser):
    """Определяет модель пользователя."""

    email = models.EmailField(
        _('email address'),
        max_length=CONST_EMAIL_LENGTH,
        unique=True
    )
    username = models.CharField(
        max_length=CONST_USERNAME_LENGTH,
        unique=True,
        validators=[
            UnicodeUsernameValidator(),
            validate_username_me
        ],
        error_messages={
            'unique': _("Пользователь с таким именем уже существует."),
        },
    )
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=CONST_ROLE_LENGTH,
        choices=[(role.value, role.label) for role in Roles],
        default=Roles.USER.value
    )
    confirmation_code = models.CharField(
        max_length=CONST_CONFIRMATION_LENGTH,
        blank=True,
        default=''
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        """Метод, который возвращает строковое представление объекта."""
        return self.username

    @property
    def is_admin(self):
        """Свойство, которое проверяет, является ли пользователь админом."""
        return self.role == Roles.ADMIN.value or self.is_staff

    @property
    def is_moderator(self):
        """
        Свойство, которое проверяет, является ли пользователь модератором.
        """
        return self.role == Roles.MODERATOR.value
