"""
URLs principales del proyecto patagonia_blog.

Enlaza el panel de administración, la autenticación y las URLs de la app blog.
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # URLs de la app blog (home, about, CRUD, búsqueda)
    path("", include("blog.urls")),
    # Autenticación (login, logout, register y rutas de password)
    path("", include("blog.auth_urls")),
]
