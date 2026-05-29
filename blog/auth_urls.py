"""
URLs de autenticación: login, logout y registro.

Usa las vistas integradas de django.contrib.auth para login/logout
y una vista propia (RegistroView) para el registro.
"""

from django.contrib.auth import views as auth_views
from django.urls import path

from .views import RegistroView

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", RegistroView.as_view(), name="register"),
]
