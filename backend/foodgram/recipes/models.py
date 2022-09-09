from django.db import models
from django.conf import settings 
from users.models import CustomUser

MAX_LENGTH = 200


class Tag(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    color = models.CharField(max_length=7)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    measurement_unit = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, related_name="ingredient_recipe", on_delete=models.CASCADE
    )
    amount = models.IntegerField()

    def __str__(self):
        return self.ingredient.name


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, verbose_name="Author"
    )
    name = models.CharField(max_length=MAX_LENGTH)
    image = models.ImageField(verbose_name="Image", upload_to='tmp_media/', blank=True)
    text = models.TextField()
    ingredients = models.ManyToManyField(IngredientRecipe, related_name="recipes")
    tags = models.ManyToManyField(Tag, related_name="recipes")
    cooking_time = models.IntegerField()

    def create(self, validated_data):
        image = validated_data.pop("image")
        recipe = Recipe.objects.create(image=image, **validated_data)
        return recipe

    def __str__(self):
        return self.name


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
        related_name="favourite_recipe",
        verbose_name="recipe",
    )


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

    def __str__(self):
        return f"{self.user} {self.following}"


# class
