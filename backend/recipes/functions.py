from .models import IngredientInRecipe


def add_tags_and_ingredients_to_recipe(recipe, tags, ingredients_amount):
    for tag in tags:
        recipe.tags.add(tag)
    all_ingredients_amount = {
        ingredient['id']: ingredient['amount']
        for ingredient in ingredients_amount
    }
    for ingredient in all_ingredients_amount:
        IngredientInRecipe.objects.create(
            recipe=recipe,
            ingredients=ingredient,
            amount=all_ingredients_amount[ingredient]
        )
