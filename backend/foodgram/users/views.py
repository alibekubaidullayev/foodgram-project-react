from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response


from .models import CustomUser
from .serializers import CustomUserSerializer


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(user=user)
