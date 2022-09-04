from djoser.serializers import UserCreateSerializer
from .models import CustomUser


class CustomUserSerializer(UserCreateSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'first_name', 'last_name')
