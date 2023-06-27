from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("pk", "email", "username", "first_name", "last_name", "password")


admin.site.register(User, UserAdmin)