import json

from django.http import HttpResponse

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from .filters import RecipeFilter
from .permissions import IsAuthorOrReadOnly
from .serializers import (
    IngredientSerializer,
    RecipeCreateSerializer,
    RecipeSerializer,
    TagSerializer,
)


FAV_CART_ARGS = {
    "methods": ["POST", "DELETE"],
    "detail": True,
    "permission_classes": (permissions.IsAuthenticated,),
}


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
    permission_classes = (IsAuthorOrReadOnly,)

    def get_serializer_class(self):
        return (
            RecipeSerializer
            if self.action in ("list", "retrieve")
            else RecipeCreateSerializer
        )

    def _favorite_cart(self, request, model):
        user = request.user
        recipe = self.get_object()
        if request.method == "POST":
            model.objects.create(user=user, recipe=recipe)
            return Response(status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            favorite = model.objects.filter(user=user, recipe=recipe)
            favorite.delete()
            return Response(status=status.HTTP_200_OK)

    @action(**FAV_CART_ARGS)
    def favorite(self, request, *args, **kwargs):
        return self._favorite_cart(request, Favorite)

    @action(**FAV_CART_ARGS)
    def shopping_cart(self, request, *args, **kwargs):
        return self._favorite_cart(request, ShoppingCart)

    @action(detail=False)
    def download_shopping_cart(self, request, *args, **kwargs):
        carts = ShoppingCart.objects.filter(user=self.request.user)
        recipes = []
        for cart in carts:
            recipes.append(cart.recipe.id)
        queryset = self.queryset.filter(id__in=recipes)
        serializer = RecipeSerializer(queryset)
        return HttpResponse(json.dumps(serializer))
