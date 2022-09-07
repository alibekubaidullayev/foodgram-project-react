import base64
import datetime as dt
from wsgiref import validate


from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag
from users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class IngredientRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(),
        write_only=True
    )
    class Meta:
        model = IngredientRecipe
        fields = ("id", "amount")


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]

            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeSerializer(many=True)
    tags = TagSerializer(many=True)
    image = Base64ImageField(
        use_url=True,
    )
    author = CustomUserSerializer()
    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "text",
            "author",
            "ingredients",
            "tags",
            "cooking_time",
        )
        read_only_fields = ("author", "tags")
    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        author = self.context.get("request").user
        recipe = Recipe.objects.create(**validated_data, author=author)
        
        for ingredient in ingredients:
            print('----------------------------------------')
            print(ingredient)
            print('----------------------------------------')            
            ingredient_instance = Ingredient.objects.get(pk=ingredient["id"].id)
            amount = ingredient["amount"]
            IngredientRecipe.objects.create(
                ingredient=ingredient_instance, amount=amount
            )
        recipe.tags.set(tags)
        return recipe
