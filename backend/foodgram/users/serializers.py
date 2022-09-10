from djoser.serializers import UserCreateSerializer
from .models import CustomUser
from rest_framework import serializers

class CustomUserSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name')

