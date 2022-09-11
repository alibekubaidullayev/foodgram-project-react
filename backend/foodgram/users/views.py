from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import Follow


class CustomUserViewSet(UserViewSet):
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
