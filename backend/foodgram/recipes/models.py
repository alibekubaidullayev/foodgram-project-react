from django.db import models

from users.models import CustomUser 

MAX_LENGTH = 200


class Tag(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    hexcolor = models.CharField(max_length=7)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    amount = models.IntegerField()
    unit = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Author'
    )
    name = models.CharField(max_length=MAX_LENGTH)
    image = models.ImageField(
        verbose_name='Image',
        upload_to='dishes/',
        blank=True
    )
    description = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient, related_name='recipes')
    tags = models.ManyToManyField(Tag, related_name='recipes')
    cooking_time_m = models.IntegerField()

    def __str__(self):
        return self.name


# class TagRecipe(models.Model):
#     tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.tag} {self.recipe}'


# class IngredientRecipe(models.Model):
#     ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
#     recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

#     def __str__(self):
#         return f'{self.ingredient} {self.recipe}'
