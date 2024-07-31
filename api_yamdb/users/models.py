from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.roles import RoleEnum
from .constants import (MAX_LENGTH_CONFIRMATION, MAX_LENGTH_EMAIL,
                        MAX_LENGTH_ROLE, MAX_LENGTH_USERNAME)
from .validators import validate_username_me


class CinemaUser(AbstractUser):
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    @property
    def is_admin(self):
        return (self.role == RoleEnum.ADMIN
                or self.is_superuser or self.is_staff)

    @property
    def is_moderator(self):
        return self.role == RoleEnum.MODERATOR

    role = models.CharField(max_length=MAX_LENGTH_ROLE,
                            choices=RoleEnum.choices,
                            default=RoleEnum.USER)

    bio = models.TextField(blank=True, null=False)

    email = models.EmailField(_('email address'),
                              max_length=MAX_LENGTH_EMAIL,
                              unique=True)

    confirmation_code = models.CharField(max_length=MAX_LENGTH_CONFIRMATION,
                                         blank=True, null=False, default='')

    username = models.CharField(
        max_length=MAX_LENGTH_USERNAME,
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
        return self.username
