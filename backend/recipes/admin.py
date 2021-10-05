from django.contrib import admin

from .models import Cart, Favorite, Ingredient, IngredientInRecipe, Recipe, Tag


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'name', 'cooking_time')
    search_fields = ('author', 'name',)
    list_filter = ('author', 'name', 'tags',)
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    search_fields = ('name',)
    list_filter = ('name', 'slug',)
    empty_value_display = '-пусто-'


@admin.register(IngredientInRecipe)
class IngredientInRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredients', 'recipe', 'amount',)
    empty_value_display = '-пусто-'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe',)
    empty_value_display = '-пусто-'
