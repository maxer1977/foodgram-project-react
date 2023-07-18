from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ("pk", "email", "username",
                    "first_name", "last_name", "password")
    search_fields = ("email", 'first_name')
    list_filter = ("email", 'first_name')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
