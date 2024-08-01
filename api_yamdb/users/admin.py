from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as UA


User = get_user_model()


@admin.register(User)
class UserAdmin(UA):
    """Регистрируем модель пользователя в административном интерфейсе"""
    list_display = ("username", "email")
