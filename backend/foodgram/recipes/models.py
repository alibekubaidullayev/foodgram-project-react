from django.contrib import admin
from django.db import models

from users.models import CustomUser

MAX_LENGTH = 200


class Tag(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name="Название")
    color = models.CharField(max_length=7, verbose_name="Цвет")
    slug = models.SlugField(unique=True, verbose_name="Слаг")

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=MAX_LENGTH, verbose_name="Название")
    measurement_unit = models.CharField(max_length=10, verbose_name="Единица")

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="Автор"
    )
    name = models.CharField(max_length=MAX_LENGTH, verbose_name="Название")
    image = models.ImageField(verbose_name="Image", upload_to="recipe")
    text = models.TextField(verbose_name="Описание")
    tags = models.ManyToManyField(Tag, related_name="recipes", verbose_name="Тэги")
    cooking_time = models.PositiveIntegerField(verbose_name="Время приготовления")

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    @admin.display(description="Count of favorite")
    def favorite_count(self):
        return Favorite.objects.filter(recipe=self).count()


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        related_name="ingredient_recipe",
        on_delete=models.CASCADE,
        verbose_name="Ингредиент",
    )
    recipe = models.ForeignKey(
        Recipe,
        related_name="ingredients",
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )
    amount = models.PositiveIntegerField(verbose_name="Количество")

    class Meta:
        verbose_name = "Ингредиент в рецепте"
        verbose_name_plural = "Ингредиенты в рецепте"
        unique_together = ("ingredient", "recipe")

    def __str__(self):
        return f"{self.amount} of {self.ingredient.name} in {self.recipe.name}"


class Favorite(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="favourite_user",
        verbose_name="user",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="is_favorited",
        verbose_name="recipe",
    )

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранные"
        unique_together = ("user", "recipe")


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="cart_owner",
        verbose_name="user",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="shopping_cart",
        verbose_name="recipe",
    )

    class Meta:
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"
        unique_together = ("user", "recipe")


class Follow(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="folllow",
        verbose_name="user",
    )

    following = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="Following"
    )

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ("user", "following")

    def __str__(self):
        return f"{self.user} {self.following}"
