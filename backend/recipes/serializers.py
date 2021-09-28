from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.serializers import CustomUserSerializer
from .models import Ingredient, Recipe, Tag, IngredientInRecipe

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    """Список ингредиентов"""
    class Meta:
        model = Ingredient
        fields = ('name', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    """Список тегов"""
    class Meta:
        model = Tag
        fields = ['name', 'slug']


class RecipeSerializer(serializers.ModelSerializer):
    """Список рецептов"""
    author = CustomUserSerializer(
        read_only=True,
    )

    ingredients = IngredientSerializer(
        many=True,
        read_only=True,
    )

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        required=False,
    )

    class Meta:
        model = Recipe
        # fields = '__all__'
        fields = ('id', 'author', 'name', 'text',
                  'ingredients', 'tags', 'image', 'cooking_time')
        # validators = {
        #     "ingredients": (
        #         UniqueIngredientsGivenValidator,
        #         IngredientsAmountIsPovitiveValidator,
        #     ),
        # }