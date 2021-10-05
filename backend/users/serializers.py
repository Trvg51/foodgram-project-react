from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from recipes.models import Recipe
from rest_framework import serializers

from .models import Follow

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username',
                  'first_name', 'last_name', 'is_subscribed')
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def get_is_subscribed(self, obj):
        if self.context['request'].user.is_authenticated:
            return Follow.objects.filter(
                user=self.context['request'].user,
                author=obj
            ).exists()
        return False


class CustomUserCreateSerializer(UserCreateSerializer):
    email = serializers.EmailField(allow_blank=False)
    first_name = serializers.CharField(allow_blank=False)
    last_name = serializers.CharField(allow_blank=False)

    class Meta():
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class RecipeSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class UserSubscribeSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta():
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_recipes(self, obj):
        queryset = obj.recipes.all()
        if self.context['request'].query_params.get('recipes_limit'):
            count_recipe = self.context[
                'request'].query_params['recipes_limit']
            queryset = obj.recipes.all()[:int(count_recipe)]
        serializer = RecipeSimpleSerializer(queryset, many=True)
        return serializer.data
