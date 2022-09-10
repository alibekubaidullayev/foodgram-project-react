from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response

from .models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    # def perform_create(self, serializer):
    #     user=self.request.user
    #     serializer.save(user=user)


    # @action(methods=['POST', 'DELETE'], detail=True)
    # def subscribe(self, request, *args, **kwargs):
    #     user = request.user
    #     recipe = self.get_object()
    #     return Response(status=status.HTTP_200_OK)

