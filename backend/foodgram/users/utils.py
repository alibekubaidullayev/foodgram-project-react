from recipes.models import Follow


def is_subscribed(self, obj):
    request = self.context.get("request")
    if not request:
        return False
    user = request.user
    if not user.is_authenticated:
        return False
    return Follow.objects.filter(user=user, following=obj).exists()
