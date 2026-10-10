from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from core.urls import preview_404

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
]

if settings.DEBUG:
    # With DEBUG on, Django shows its own technical 404. This lets you preview ours.
    urlpatterns += [path("preview-404/", preview_404)]

handler404 = "django.views.defaults.page_not_found"
handler500 = "django.views.defaults.server_error"
