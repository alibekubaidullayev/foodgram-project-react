from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("api/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.authtoken")),
    path(
        "api/docs/",
        TemplateView.as_view(template_name="redoc.html"),
        name="redoc"
    ),
]


if settings.DEBUG:
    stat = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += stat
