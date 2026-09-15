from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path("", include("cv.urls")),
]

urlpatterns += [
    path(
        "pdf-cv/<path:path>",
        serve,
        {"document_root": settings.BASE_DIR / "pdf-cv"},
    )
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
