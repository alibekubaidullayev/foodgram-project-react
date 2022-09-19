from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from recipes.models import Recipe
from .models import CustomUser
from .utils import is_subscribed


class CustomUserSerializer(UserCreateSerializer):

    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        return is_subscribed(self, obj)

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "is_subscribed",
        )


class RecipeSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )


class CustomUserSubscriptionSerializer(UserCreateSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    def get_recipes(self, obj):
        request = self.context.get("request")
        recipes = Recipe.objects.filter(author=obj)
        data = RecipeSubscriptionSerializer(
            recipes, many=True, context={"request": request}
        ).data[:3]
        return data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_is_subscribed(self, obj):
        return is_subscribed(self, obj)

    class Meta:
        model = CustomUser
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
            "recipes",
            "recipes_count",
        )
