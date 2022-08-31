from rest_framework import viewsets

from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import SAFE_METHODS, AllowAny


from recipes.models import (
    CONFIRMATION_CODE_LENGTH, User, Tag, Ingredient, Recipe)

from .permissions import (IsAdmin, IsAdminOrReadOnly)
from .serializers import (UserSerializer, TagSerializer,
                          IngredientSerializer, RecipeSerializer)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination

    @action(
        methods=['get', 'patch'],
        url_path='me',
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def user_profile(self, request):
        if request.method != 'PATCH':
            return Response(self.get_serializer(request.user).data)
        serializer = self.get_serializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
