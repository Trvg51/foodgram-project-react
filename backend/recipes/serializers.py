from drf_base64.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.serializers import CustomUserSerializer
from .functions import add_tags_and_ingredients_to_recipe
from .models import Cart, Favorite, Ingredient, IngredientInRecipe, Recipe, Tag


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredients.id')
    name = serializers.ReadOnlyField(source='ingredients.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredients.measurement_unit')
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = '__all__'


class IngredientInRecipeCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = ('id', 'amount',)


class RecipeListSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)
    ingredients = IngredientInRecipeSerializer(
        many=True, source='ingredients_amount')

    class Meta:
        model = Recipe
        fields = (
            'id',
            'author',
            'tags',
            'is_favorited',
            'is_in_shopping_cart',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def get_is_favorited(self, obj):
        if self.context['request'].user.is_authenticated:
            return Favorite.objects.filter(
                user=self.context['request'].user,
                recipe=obj).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        if self.context['request'].user.is_authenticated:
            return Cart.objects.filter(
                user=self.context['request'].user,
                recipe=obj).exists()
        return False


class RecipeCreateSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    ingredients = IngredientInRecipeCreateSerializer(many=True)
    image = Base64ImageField(required=True)
    cooking_time = serializers.IntegerField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )

    def validate_tags(self, data):
        tags = self.initial_data.get('tags')
        len_tags = len(tags)
        if len_tags == 0:
            raise serializers.ValidationError('Добавьте минимум 1 тэг')
        if len_tags > len(set(tags)):
            raise serializers.ValidationError('Тэги не должны повторяться')
        return data

    def validate_ingredients(self, data):
        ingredients = self.initial_data.get('ingredients')
        if len(ingredients) == 0:
            raise ValidationError('Добавьте ингредиент')
        ingredients_list = []
        for item in ingredients:
            try:
                amount = int(item.get('amount'))
            except ValueError:
                raise serializers.ValidationError(
                    'Правильно укажите количество')
            if amount <= 0:
                raise serializers.ValidationError(
                    'Количество должно быть > 0')
            elif item['id'] in ingredients_list:
                raise serializers.ValidationError('Проверьте, что ингредиенты '
                                                  'не повторяются')
            else:
                ingredients_list.append(item['id'])
        return data

    def validate_cooking_time(self, data):
        if data <= 0:
            raise ValidationError(
                'Время приготовления не может быть меньше 1')
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        tags = validated_data.pop('tags')
        ingredients_amount = validated_data.pop('ingredients')
        new_recipe = Recipe.objects.create(
            author=user,
            **validated_data
        )
        add_tags_and_ingredients_to_recipe(
            new_recipe, tags, ingredients_amount)
        return new_recipe

    def update(self, update_recipe, validated_data):
        tags = validated_data.pop('tags')
        ingredients_amount = validated_data.pop('ingredients')
        Recipe.objects.filter(id=update_recipe.id).update(**validated_data)
        update_recipe.refresh_from_db()
        update_recipe.tags.clear()
        update_recipe.ingredients.clear()
        add_tags_and_ingredients_to_recipe(
            update_recipe, tags, ingredients_amount)
        return update_recipe

    def to_representation(self, instance):
        return RecipeListSerializer(
            instance,
            context={
                'request': self.context.get('request')
            }
        ).data


class FavoriteSerializer(RecipeListSerializer):

    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
