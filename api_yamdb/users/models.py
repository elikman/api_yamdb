from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.roles import Roles
from .constants import (
    CONST_ROLE_LENGTH,
    CONST_EMAIL_LENGTH,
    CONST_CONFIRMATION_LENGTH,
    CONST_USERNAME_LENGTH,)
from .validators import validate_username_me


class CinemaUser(AbstractUser):
    """Определяем модель пользователя"""
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    @property
    def is_admin(self):
        """Свойство, которое проверяет, является ли пользователь админом"""
        return (self.role == Roles.ADMIN.value
                or self.is_superuser or self.is_staff)

    @property
    def is_moderator(self):
        """Свойство, которое проверяет, является ли пользователь модератором"""
        return self.role == Roles.MODERATOR.value

    role = models.CharField(max_length=CONST_ROLE_LENGTH,
                            choices=[(role.value, role.label)
                                     for role in Roles],
                            default=Roles.USER.value)

    bio = models.TextField(blank=True, null=False)

    email = models.EmailField(_('email address'),
                              max_length=CONST_EMAIL_LENGTH,
                              unique=True)

    confirmation_code = models.CharField(max_length=CONST_CONFIRMATION_LENGTH,
                                         blank=True, null=False, default='')

    username = models.CharField(
        max_length=CONST_USERNAME_LENGTH,
        unique=True,
        validators=[
            UnicodeUsernameValidator(),
            validate_username_me
        ],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    def __str__(self):
        """Метод, который возвращает строковое представление объекта"""
        return self.username
