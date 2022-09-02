from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from users.models import User

MAX_LENGTH = 200

User = get_user_model()

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
    ingredients = models.ManyToManyField(
        Ingredient, related_name='recipes', blank=True)
    tags = models.ManyToManyField(Tag, related_name='recipes', blank=True)
    cooking_time_m = models.IntegerField()

    def __str__(self):
        return self.name