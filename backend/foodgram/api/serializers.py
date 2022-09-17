from rest_framework import serializers

from recipes.models import (
    Favorite,
    Ingredient,
    IngredientRecipe,
    Recipe,
    ShoppingCart,
    Tag,
)
from users.serializers import CustomUserSerializer
from .utils import Base64ImageField


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "color", "slug")


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ("id", "name", "measurement_unit")


class IngredientRecipeCreateSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), write_only=True
    )

    class Meta:
        model = IngredientRecipe
        fields = ("id", "amount")


class IngredientRecipeSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(
        source="ingredient.name",
        read_only=True
    )
    measurement_unit = serializers.StringRelatedField(
        source="ingredient.measurement_unit", read_only=True
    )
    id = serializers.IntegerField(source="ingredient_id", read_only=True)

    class Meta:
        model = IngredientRecipe
        fields = ("id", "name", "measurement_unit", "amount")


class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientRecipeSerializer(many=True)
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()

    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        request = self.context.get("request")
        if not request:
            return False
        user = request.user
        if not user.is_authenticated:
            return False

        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        if not request:
            return False
        user = request.user
        if not user.is_authenticated:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favorited",
            "is_in_shopping_cart",
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
    ingredients = IngredientRecipeCreateSerializer(many=True)

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

    def validate(self, data):
        unique_ingredients = set()
        for ingredient in data["ingredients"]:
            if ingredient in unique_ingredients:
                raise serializers.ValidationError("Найден дубликат ингредиент")
            unique_ingredients.add(ingredient)

        unique_tags = set()
        for tag in range(len(data["tags"])):
            if tag in unique_tags:
                raise serializers.ValidationError("Найден дубликат тэга")
            unique_tags.add(tag)
        return data

    def _ingredients_save(self, recipe, ingredients):
        objs = (
            IngredientRecipe(
                recipe=recipe,
                ingredient=ingredient["id"],
                amount=ingredient["amount"]
            )
            for ingredient in ingredients
        )
        IngredientRecipe.objects.bulk_create(objs)

    def create(self, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        author = self.context.get("request").user
        recipe = Recipe.objects.create(**validated_data, author=author)
        recipe.tags.set(tags)
        self._ingredients_save(recipe, ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop("ingredients")
        tags = validated_data.pop("tags")
        super().update(instance, validated_data)
        IngredientRecipe.objects.filter(recipe=instance).delete()
        self._ingredients_save(instance, ingredients)
        instance.tags.set(tags)
        return instance
