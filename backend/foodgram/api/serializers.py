import base64
import datetime as dt
from wsgiref import validate


from django.core.files.base import ContentFile
from rest_framework import serializers

from recipes.models import Ingredient, IngredientRecipe, Recipe, Tag, Favorite
from users.models import CustomUser
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
        queryset=Ingredient.objects.all(), write_only=True
    )

    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        name = Ingredient.objects.filter(pk=obj.ingredient_id).values()[0]['name']
        return name

    class Meta:
        model = IngredientRecipe
        fields = ("id", "amount", "name")


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
    author = CustomUserSerializer()

    is_favorited = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        request = self.context.get('request', None)
        user = request.user
        if not isinstance(user, CustomUser):
            return False

        return Favorite.objects.filter(user=user, recipe=obj).exists()

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
            "is_favorited"
        )
        read_only_fields = ("author", "tags")


class RecipeCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField(
        use_url=True,
    )
    ingredients = IngredientRecipeSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "text",
            "ingredients",
            "tags",
            "cooking_time",
            "author",
        )
        read_only_fields = ("author",)

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        author = self.context.get("request").user
        recipe = Recipe.objects.create(**validated_data, author=author)
        for ingredient in ingredients:
            ingredient_instance = Ingredient.objects.get(pk=ingredient["id"].id)
            amount = ingredient["amount"]
            ingr = IngredientRecipe.objects.create(
                ingredient=ingredient_instance, amount=amount
            )
            recipe.ingredients.add(ingr)
        recipe.tags.set(tags)
        return recipe
