from recipes.models import (CONFIRMATION_CODE_LENGTH, EMAIL_LENGTH,
                            USERNAME_LENGTH, Ingredient, Recipe, Tag, User)
from recipes.validators import UsernameValidation
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer, UsernameValidation):
    class Meta:
        model = User
    fields = (
        'username', 'first_name', 'last_name', 'email', 'role', 'bio'
    )


class SignUpSerializer(serializers.Serializer, UsernameValidation):
    username = serializers.CharField(max_length=USERNAME_LENGTH,)
    email = serializers.EmailField(max_length=EMAIL_LENGTH,)


class TokenSerializer(serializers.Serializer, UsernameValidation):
    username = serializers.CharField(max_length=USERNAME_LENGTH,)
    confirmation_code = serializers.CharField(
        max_length=CONFIRMATION_CODE_LENGTH
    )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'hexcolor', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('name', 'amount', 'unit')


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer()
    tags = TagSerializer(many=True)

    class Meta:
        model = Recipe
        read_only_fields = ('__all__',)
        fields = ('author', 'name', 'description',
                  'ingredients', 'tags', 'cooking_time_m')


class RecipePostEditSerializer(serializers.ModelSerializer):
    tags = serializers.SlugRelatedField(
        many=True, slug_field='slug', queryset=Tag.objects.all()
    )
    ingerdient = IngredientSerializer()

    class Meta:
        model = Recipe
        fields = ('name', 'description', 'cooking_time_m')
