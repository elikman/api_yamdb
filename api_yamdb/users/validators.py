from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_username_me(value):
    if value.lower() == 'me':
        raise ValidationError(
            _('Username cannot be "me".'),
            params={'value': value},
        )
