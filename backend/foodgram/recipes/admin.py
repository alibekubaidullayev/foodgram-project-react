from django.contrib import admin

from users.models import CustomUser

from .models import Ingredient, Recipe, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    empty_value_display = "-пусто-"


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "measurement_unit")
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    fields = ("author", "name", "text", "cooking_time", "tags")
    list_display = ("author", "name", "text", "cooking_time", "favorite_count")
    search_fields = ("name",)
    list_filter = ("name", "author", "tags")
    empty_value_display = "-пусто-"


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")
    search_fields = ("username", "email")
    list_filter = ("username", "email")
    empty_value_display = "-пусто-"
