from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка для USER."""

    list_display = ("pk", "email", "username", "first_name", "last_name", "password")
    search_fields = ("email", "first_name")
    list_filter = ("email", "first_name")
    empty_value_display = "-пусто-"
