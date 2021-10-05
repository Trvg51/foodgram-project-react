import base64

from django.contrib.auth import get_user_model
from django.core.files import base, images
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import APIException, ValidationError
from users.serializers import CustomUserSerializer

from .models import Ingredient, IngredientInRecipe, Recipe, Tag

User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
    """Список ингредиентов"""
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    """Список тегов"""
    class Meta:
        model = Tag
        fields = '__all__'


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
