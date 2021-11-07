from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import IngredientsFilter, RecipeFilter
from .models import Cart, Favorite, Ingredient, IngredientInRecipe, Recipe, Tag
from .pagination import PageNumberPaginator
from .permissions import IsOwnerOrAdminOrReadOnly
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeListSerializer, TagSerializer)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all().order_by('name')
    serializer_class = IngredientSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = IngredientsFilter
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-id')
    serializer_class = RecipeListSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = PageNumberPaginator
    http_method_names = ['get', 'post', 'put', 'patch', 'head', 'delete']

    def get_serializer_class(self):
        if (self.action == 'create' or
                self.action == 'update' or
                self.action == 'partial_update'):
            return RecipeCreateSerializer
        elif self.action == 'list':
            return RecipeListSerializer
        return self.serializer_class

    @action(
        methods=['GET', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated],
        detail=True)
    def favorite(self, request, pk):
        if request.method == 'GET':
            recipe = get_object_or_404(Recipe, id=pk)
            is_favorite = Favorite.objects.filter(
                user=request.user,
                recipe=recipe)
            if is_favorite.exists():
                return Response(
                    {'error': 'Рецепт уже в избранном'},
                    status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(
                user=request.user,
                recipe=recipe)
            return Response(
                {
                    'id': str(recipe.id),
                    'name': str(recipe.name),
                    'image': request.build_absolute_uri(recipe.image.url),
                    'cooking_time': str(recipe.cooking_time)
                },
                status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, id=pk)
            is_favorite = Favorite.objects.filter(
                user=request.user,
                recipe=recipe)
            if is_favorite.exists():
                is_favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error':
                    'Вы не можете удалить рецепт, так как '
                    'его нет в избранном'},
                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'error': 'Ошибка запроса'},
                status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['GET', 'DELETE'],
        permission_classes=[permissions.IsAuthenticated],
        detail=True)
    def shopping_cart(self, request, pk):
        if request.method == 'GET':
            recipe = get_object_or_404(Recipe, id=pk)
            shopping_cart = Cart.objects.filter(
                user=request.user,
                recipe=recipe)
            if shopping_cart.exists():
                return Response(
                    {'error': 'Рецепт уже находится в списке покупок'},
                    status=status.HTTP_400_BAD_REQUEST)
            Cart.objects.create(
                user=request.user,
                recipe=recipe)
            return Response(
                {
                    'id': str(recipe.id),
                    'name': str(recipe.name),
                    'image': request.build_absolute_uri(recipe.image.url),
                    'cooking_time': str(recipe.cooking_time)
                },
                status=status.HTTP_201_CREATED)
        elif request.method == 'DELETE':
            recipe = get_object_or_404(Recipe, id=pk)
            shopping_cart = Cart.objects.filter(
                user=request.user,
                recipe=recipe)
            if shopping_cart.exists():
                shopping_cart.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response(
                {'error':
                    'Вы не можете удалить рецепт, так как '
                    'его нет в списке покупок'},
                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'error': 'Ошибка запроса'},
                status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['GET'],
        permission_classes=[permissions.IsAuthenticated],
        detail=False)
    def download_shopping_cart(self, request):
        all_ingredients = IngredientInRecipe.objects.filter(
            recipe__shop_cart__user=request.user).values_list(
                'ingredients__name', 'amount', 'ingredients__measurement_unit')
        amount_ingredients = all_ingredients.values(
            'ingredients__name', 'ingredients__measurement_unit').annotate(
                total=Sum('amount')).order_by('-total')

        shop_list = [f'Список покупок {request.user} \n \n']
        for ingredient in amount_ingredients:
            shop_list.append(
                f'{ingredient["ingredients__name"]} - '
                f'{ingredient["total"]} '
                f'{ingredient["ingredients__measurement_unit"]} \n'
            )
        response = HttpResponse(shop_list, 'Content-Type: text/plain')
        response[
            'Content-Disposition'] = 'attachment; filename="shop_list.txt"'
        return response
