from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from django.core import serializers
import json
from .filters import RecipeFilter
from .serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeSerializer,
    TagSerializer,
)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        queryset = Recipe.objects.all()
        is_favorited = self.request.query_params.get("is_favorited")
        is_in_shopping_cart = self.request.query_params.get("is_in_shopping_cart")
        if is_favorited:
            favorites = Favorite.objects.filter(user=self.request.user)
            recipes = []
            for favorite in favorites:
                recipes.append(favorite.recipe.id)
            queryset = queryset.filter(id__in=recipes)

        if is_in_shopping_cart:
            carts = ShoppingCart.objects.filter(owner=self.request.user)
            recipes = []
            for cart in carts:
                recipes.append(cart.recipe.id)
            queryset = queryset.filter(id__in=recipes)

        return queryset

    def get_serializer_class(self):
        return (
            RecipeSerializer
            if self.action in ("list", "retrieve")
            else RecipeCreateSerializer
        )

    @action(methods=["POST", "DELETE"], detail=True)
    def favorite(self, request, *args, **kwargs):
        user = request.user
        recipe = self.get_object()
        if request.method == "POST":
            Favorite.objects.create(user=user, recipe=recipe)
            return Response(status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            favorite = Favorite.objects.filter(user=user, recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_200_OK)

    @action(methods=["POST", "DELETE"], detail=True)
    def shopping_cart(self, request, *args, **kwargs):
        user = request.user
        recipe = self.get_object()
        if request.method == "POST":
            ShoppingCart.objects.create(owner=user, recipe=recipe)
            return Response(status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            cart = ShoppingCart.objects.filter(owner=user, recipe=recipe)
            cart.delete()
            return Response(status=status.HTTP_200_OK)

    @action(detail=False)
    def download_shopping_cart(self, request, *args, **kwargs):
        carts = ShoppingCart.objects.filter(owner=self.request.user)
        recipes = []
        for cart in carts:
            recipes.append(cart.recipe.id)
        queryset = self.queryset.filter(id__in=recipes)
        serializer = RecipeSerializer(queryset)
        return HttpResponse(json.dumps(serializer), content_type="application/json")

    def perform_update(self, serializer, pk=None):
        instance = self.get_object()
        if self.request.user.is_authenticated:
            updated_instance = serializer.save(author=self.request.user)
        else:
            updated_instance = serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
