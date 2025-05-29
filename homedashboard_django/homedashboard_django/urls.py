from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .health import health_check

urlpatterns = [
    path("admin/", admin.site.urls),
    path("health/", health_check),
    path("api/account/", include("apps.core.account.urls")),
    path("api/catalog/", include("apps.services.catalog.urls")),
    path("api/maintenance/", include("apps.services.maintenance.urls")),
    path("api/audiowatch/", include("apps.infra.audiowatch.urls")),
    path("api/monitoring/", include("apps.infra.monitoring.urls")),
    path("apps/", include("apps.services.apps.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
