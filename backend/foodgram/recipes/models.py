from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

MAX_LENGTH = 200
USER = 'user'
ADMIN = 'admin'
USERNAME_LENGTH = 150
EMAIL_LENGTH = 254
CONFIRMATION_CODE_LENGTH = 6

ROLES = {
    (USER, 'User'),
    (ADMIN, 'Administrator')
}


class User(AbstractUser):
    username = models.CharField(
        'User name',
        max_length=USERNAME_LENGTH,
        unique=True,
    )
    email = models.EmailField(
        max_length=EMAIL_LENGTH,
        unique=True,
        verbose_name='Mail'
    )
    first_name = models.CharField(
        'First Name',
        max_length=USERNAME_LENGTH,
        blank=True,
        null=True
    )
    last_name = models.CharField(
        'Surname',
        max_length=USERNAME_LENGTH,
        blank=True,
        null=True
    )
    role = models.CharField(
        verbose_name='Role',
        max_length=10,
        choices=ROLES,
        default=USER
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Bio'
    )
    confirmation_code = models.CharField(
        'Confirmation Code',
        max_length=CONFIRMATION_CODE_LENGTH,
        blank=True
    )

    def is_admin(self):
        return self.role == ADMIN

    class Meta:
        ordering = ['username', ]
        verbose_name = 'user'
        verbose_name_plural = 'users'


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
    # image = models.ImageField(
    #     verbose_name='Image',
    #     upload_to='dishes/',
    #     blank=True
    # )
    description = models.TextField()
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes', blank=True)
    tags = models.ManyToManyField(Tag, related_name='recipes', blank=True)
    cooking_time_m = models.IntegerField()
