import base64

from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes.models import Favorite, Ingredient, IngredientRecipe, Recipe, Tag
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
    name = serializers.SerializerMethodField()
    measurement_unit = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.ingredient_id

    def get_name(self, obj):
        ingredient = Ingredient.objects.filter(pk=obj.ingredient_id)
        name = ingredient.values()[0]["name"]
        return name

    def get_measurement_unit(self, obj):
        unit = Ingredient.objects.filter(pk=obj.ingredient_id).values()[0][
            "measurement_unit"
        ]
        return unit

    class Meta:
        model = IngredientRecipe
        fields = ("id", "name", "measurement_unit", "amount")


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
        request = self.context.get("request", None)
        user = request.user
        if not isinstance(user, CustomUser):
            return False

        return Favorite.objects.filter(user=user, recipe=obj).exists()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "name",
            "image",
            "text",
            "cooking_time",
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
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        )
        read_only_fields = ("author",)

    def create(self, validated_data):
        validated_data.pop("ingredients")
        ingredients = self.initial_data.get("ingredients")
        tags = validated_data.pop("tags")
        author = self.context.get("request").user
        recipe = Recipe.objects.create(**validated_data, author=author)
        recipe.tags.set(tags)
        for ingredient in ingredients:
            ingredient_pk = int(ingredient["id"])
            ingredient_origin = get_object_or_404(Ingredient, pk=ingredient_pk)
            amount = ingredient["amount"]
            IngredientRecipe.objects.create(
                recipe=recipe, ingredient=ingredient_origin, amount=amount
            )
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.image = validated_data.get("image", instance.image)
        instance.text = validated_data.get("text", instance.text)
        instance.cooking_time = validated_data.get(
            "cooking_time", instance.cooking_time
        )
        ingredients = self.initial_data.get("ingredients")
        tags = self.initial_data.get("tags")
        instance.tags.set(tags)
        IngredientRecipe.objects.filter(recipe=instance).delete()
        for ingredient in ingredients:
            ingredient_pk = int(ingredient["id"])
            ingredient_origin = get_object_or_404(Ingredient, pk=ingredient_pk)
            IngredientRecipe.objects.create(
                recipe=instance,
                ingredient=ingredient_origin,
                amount=ingredient["amount"],
            )
        instance.save()
        return instance
