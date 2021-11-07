import django_filters

from .models import Ingredient, Recipe


class IngredientsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(django_filters.FilterSet):

    is_in_shopping_cart = django_filters.BooleanFilter(
        method='get_in_cart',
    )
    is_favorited = django_filters.BooleanFilter(
        method='get_is_favorited',
    )
    tags = django_filters.AllValuesMultipleFilter(
        field_name='tags__slug',
    )

    class Meta:
        model = Recipe
        fields = (
            'author',
            'is_in_shopping_cart',
            'is_favorited',
            'tags',
        )

    def get_in_cart(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(shop_cart__user=self.request.user)
        return Recipe.objects.all()

    def get_is_favorited(self, queryset, name, value):
        if value:
            return Recipe.objects.filter(
                favorite_recipe_for_user__user=self.request.user)
        return Recipe.objects.all()
