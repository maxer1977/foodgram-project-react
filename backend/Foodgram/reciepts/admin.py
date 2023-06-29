from django.contrib import admin

from .models import Ingridients, Tags, Reciepts, Subscriptions, Favorits, Shopping, Ingridient_lists


class IngridientsAdmin(admin.ModelAdmin):
    list_display = ("pk", "ingridient", "measure")
    search_fields = ("ingridient",)
    list_filter = ("ingridient",)
    empty_value_display = '-пусто-'


class TagsAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "color", "slug")
    search_fields = ("name", "slug")
    list_filter = ("name", "slug")
    empty_value_display = '-пусто-'


class RecieptsAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "title", "pub_date", "text", "duration", "image")
    search_fields = ("author", "title", "text")
    list_filter = ("author", "title")
    empty_value_display = '-пусто-'


class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "user")
    search_fields = ("author", "user")
    list_filter = ("author", "user")
    empty_value_display = '-пусто-'


class FavoritsAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "reciept")
    search_fields = ("user", "reciept")
    list_filter = ("user", "reciept")
    empty_value_display = '-пусто-'


class ShoppingAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "reciept")
    search_fields = ("user", "reciept")
    list_filter = ("user", "reciept")
    empty_value_display = '-пусто-'


class Ingridient_listsAdmin(admin.ModelAdmin):
    list_display = ("pk", "reciept", "ingridient", "quantity")
    search_fields = ("reciept", "ingridient")
    list_filter = ("reciept", "ingridient")
    empty_value_display = '-пусто-'


admin.site.register(Ingridients, IngridientsAdmin)
admin.site.register(Tags, TagsAdmin)
admin.site.register(Reciepts, RecieptsAdmin)
admin.site.register(Subscriptions,SubscriptionsAdmin)
admin.site.register(Favorits, FavoritsAdmin)
admin.site.register(Shopping, ShoppingAdmin)
admin.site.register(Ingridient_lists, Ingridient_listsAdmin)
