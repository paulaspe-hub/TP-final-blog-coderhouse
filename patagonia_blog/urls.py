"""
URLs principales del proyecto patagonia_blog.

Enlaza el panel de administración, la autenticación y las URLs de la app blog.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("blog.urls")),

    path("", include("blog.auth_urls")),
]
