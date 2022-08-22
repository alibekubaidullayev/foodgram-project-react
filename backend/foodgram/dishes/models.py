from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=200)
    hexcolor = models.CharField(max_length=7)
    slug = models.SlugField(unique=True)


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    amount = models.IntegerField()
    unit = models.CharField(max_length=10)


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Author'
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(
        verbose_name='Image',
        upload_to='dishes/',
        blank=True
    )
    description = models.TextField()
