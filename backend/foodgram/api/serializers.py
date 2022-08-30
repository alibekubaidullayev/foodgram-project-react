from rest_framework import serializers

from recipes.models import User, Tag, Ingredient, Recipe


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
    fields = (
        'username', 'first_name', 'last_name', 'email', 'role', 'bio'
    )


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
