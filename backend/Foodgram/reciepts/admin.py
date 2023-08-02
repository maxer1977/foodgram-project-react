from django.contrib import admin

from .models import (
    Favorits,
    IngridientList,
    Ingridients,
    Reciepts,
    Shopping,
    Subscriptions,
    Tags,
)


@admin.register(Ingridients)
class IngridientsAdmin(admin.ModelAdmin):
    list_display = ("pk", "ingridient", "measure")
    search_fields = ("ingridient",)
    list_filter = ("ingridient",)
    empty_value_display = "-пусто-"


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "color", "slug")
    search_fields = ("name", "slug")
    list_filter = ("name", "slug")
    empty_value_display = "-пусто-"


@admin.register(Reciepts)
class RecieptsAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "title", "pub_date",
                    "text", "duration", "image")
    search_fields = ("author", "title", "text")
    list_filter = ("author", "title")
    empty_value_display = "-пусто-"


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "user")
    search_fields = ("author", "user")
    list_filter = ("author", "user")
    empty_value_display = "-пусто-"


@admin.register(Favorits)
class FavoritsAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "reciept")
    search_fields = ("user", "reciept")
    list_filter = ("user", "reciept")
    empty_value_display = "-пусто-"


@admin.register(Shopping)
class ShoppingAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "reciept")
    search_fields = ("user", "reciept")
    list_filter = ("user", "reciept")
    empty_value_display = "-пусто-"


@admin.register(IngridientList)
class IngridientListAdmin(admin.ModelAdmin):
    list_display = ("pk", "reciept", "ingridient", "quantity")
    search_fields = ("reciept", "ingridient")
    list_filter = ("reciept", "ingridient")
    empty_value_display = "-пусто-"
