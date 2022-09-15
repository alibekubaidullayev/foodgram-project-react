from djoser.views import UserViewSet
from rest_framework import pagination, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import Follow

from .models import CustomUser
from .serializers import CustomUserSubscriptionSerializer


class CustomUserViewSet(UserViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = pagination.PageNumberPagination

    @action(detail=False)
    def subscriptions(self, request, *args, **kwargs):
        follows = Follow.objects.filter(user=request.user)
        authors = follows.values_list("following", flat=True)
        authors = CustomUser.objects.filter(id__in=authors)
        serializer = CustomUserSubscriptionSerializer(
            authors, many=True, context={"request": request}
        )
        data = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(data)

    @action(methods=["POST", "DELETE"], detail=True)
    def subscribe(self, request, *args, **kwargs):
        author = self.get_object()
        if request.method == "POST":
            Follow.objects.create(user=request.user, following=author)
            return Response(status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            follow = Follow.objects.filter(user=request.user, following=author)
            follow.delete()
            return Response(status=status.HTTP_200_OK)
