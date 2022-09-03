from django.urls import include, path
from .views import CustomUserViewSet

app_name = 'users'

urlpatterns = [
   path('register', CustomUserViewSet.as_view({'post': 'create'}), name='register'),
    
]
