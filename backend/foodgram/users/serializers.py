from djoser.serializers import UserCreateSerializer
from .models import CustomUser
from rest_framework import serializers

from recipes.models import Follow

class CustomUserSerializer(UserCreateSerializer):
    
    is_subscribed = serializers.SerializerMethodField()

    
    def get_is_subscribed(self, obj):
        request = self.context.get("request", None)
        user = request.user
        if not isinstance(user, CustomUser):
            return False

        return Follow.objects.filter(user=user, following=obj).exists()

    class Meta:
        model = CustomUser
        fields = (
            "id",
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "is_subscribed",
        )
