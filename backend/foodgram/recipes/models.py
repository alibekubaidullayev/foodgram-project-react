from unittest.util import _MAX_LENGTH
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

MAX_LENGTH = 200


class Tag(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    hexcolor = models.CharField(max_length=7)
    slug = models.SlugField(unique=True)


class Ingredient(models.Model):
    name = models.CharField(max_length=MAX_LENGTH)
    amount = models.IntegerField()
    unit = models.CharField(max_length=10)


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
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
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    tags = models.ManyToManyField(Tag, related_name='recipes')
    cooking_time_m = models.IntegerField()
