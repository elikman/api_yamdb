from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email")
    add_fieldsets = (
        (None, {'fields': (
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'bio',
            'role')}),
    )
