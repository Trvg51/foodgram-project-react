from colorfield.fields import ColorField
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингредиента',
        max_length=50,
    )

    measurement_unit = models.CharField(
        verbose_name='Единицы измерения',
        max_length=20,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}({self.measurement_unit})'


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=40,
        null=False,
        unique=True,
    )
    color = ColorField(
        verbose_name='Уникальный цвет',
        format='hexa',
        null=False,
        unique=True,

    )
    slug = models.SlugField(
        max_length=40,
        null=False,
        unique=True,
        verbose_name='"slug" тэга',
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=100,
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/images/',
        blank=False,
        null=False
    )
    text = models.TextField(
        verbose_name='Описание',
        null=False
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты в рецепте',
        through='IngredientInRecipe',
        blank=False,
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег рецепта',
        related_name='recipes',
        blank=False
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления (мин.)',
        blank=False
    )
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    ingredients = models.ForeignKey(
        Ingredient,
        verbose_name='Ингредиенты',
        on_delete=models.PROTECT,
        blank=False,
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт ингредиента',
        on_delete=models.CASCADE,
        blank=False,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиента',
        null=False,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        verbose_name = 'Ингредиенты в рецепте'
        verbose_name_plural = 'Ингредиенты в рецепте'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredients'],
                name='uniq_ingred_amount'
            )
        ]

    def __str__(self):
        return (f'Понадобится {self.amount}'
                f'{self.ingredients.measurement_unit}. '
                f'"{self.ingredients.name}"'
                f' для "{self.recipe}"')


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shop_cart',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='shop_cart',
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='recipe in user`s cart',
            )
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в корзине пользователя {self.user}'


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Избранное у пользователя',
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Избранный рецепт',
        on_delete=models.CASCADE,
        related_name='favorite_recipe_for_user',
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='uniq_fav_recipes',
            )
        ]

    def __str__(self):
        return (f'Избранный рецепт - `{self.recipe}`,'
                'у пользователя {self.user}')
