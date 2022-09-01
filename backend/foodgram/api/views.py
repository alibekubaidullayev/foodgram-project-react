from django.core.mail import send_mail
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from recipes.models import (CONFIRMATION_CODE_LENGTH, Ingredient, Recipe, Tag,
                            User)
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import SAFE_METHODS, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings

from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import (IngredientSerializer, RecipeSerializer,
                          SignUpSerializer, TagSerializer, TokenSerializer,
                          UserSerializer)

USERNAME_EMAIL_ALREADY_EXISTS = 'Такое username или email уже занято.'
CORRECT_CODE_EMAIL_MESSAGE = 'Код подтверждения: {code}.'
INVALID_CODE = 'Неверный код подтверждения.'


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

@api_view(['POST'])
@permission_classes((AllowAny,))
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(
            email=serializer.validated_data.get('email'),
            username=serializer.validated_data.get('username'),
        )
    except IntegrityError:
        return Response(
            USERNAME_EMAIL_ALREADY_EXISTS,
            status=status.HTTP_400_BAD_REQUEST
        )
    user.confirmation_code = get_random_string(length=CONFIRMATION_CODE_LENGTH)
    user.save()
    send_mail(
        subject='Код регистрации на сервисе YaMDb',
        message=CORRECT_CODE_EMAIL_MESSAGE.format(
            code=user.confirmation_code
        ),
        from_email='webmaster@localhost',
        recipient_list=[user.email, ],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def get_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data.get('username')
    )
    if (user.confirmation_code == serializer.validated_data.get(
            'confirmation_code'
    )) and user.confirmation_code:
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODEHANDLER
        payload = jwt_payload_handler(request.user)
        token = jwt_encode_handler(payload)
        return Response({'token': token}, status=status.HTTP_200_OK)
    user.confirmation_code = ''
    user.save()
    return Response(INVALID_CODE, status=status.HTTP_400_BAD_REQUEST)


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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
