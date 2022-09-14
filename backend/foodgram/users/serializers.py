from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from recipes.models import Follow, Recipe

from .models import CustomUser


class CustomUserSerializer(UserCreateSerializer):

    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get("request", None)
        if not request:
            return False
        user = request.user
        if not isinstance(user, CustomUser):
            return False

        return Follow.objects.filter(user=user, following=obj).exists()

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
        ).data
        return data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_is_subscribed(self, obj):
        request = self.context.get("request", None)
        if not request:
            return False
        user = request.user
        if not isinstance(user, CustomUser):
            return False

        return Follow.objects.filter(user=user, following=obj).exists()

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
