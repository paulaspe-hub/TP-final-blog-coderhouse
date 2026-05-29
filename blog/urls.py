"""
URLs de la app blog: home, about y CRUD de los tres modelos.
"""

from django.urls import path

from . import views

urlpatterns = [

    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),

    path("tipos/", views.TipoLugarListView.as_view(), name="tipolugar_list"),
    path("tipos/nuevo/", views.TipoLugarCreateView.as_view(), name="tipolugar_create"),
    path(
        "tipos/<int:pk>/editar/",
        views.TipoLugarUpdateView.as_view(),
        name="tipolugar_update",
    ),
    path(
        "tipos/<int:pk>/eliminar/",
        views.TipoLugarDeleteView.as_view(),
        name="tipolugar_delete",
    ),

    path("lugares/", views.LugarListView.as_view(), name="lugar_list"),
    path("lugares/nuevo/", views.LugarCreateView.as_view(), name="lugar_create"),
    path("lugares/<int:pk>/", views.LugarDetailView.as_view(), name="lugar_detail"),
    path(
        "lugares/<int:pk>/editar/",
        views.LugarUpdateView.as_view(),
        name="lugar_update",
    ),
    path(
        "lugares/<int:pk>/eliminar/",
        views.LugarDeleteView.as_view(),
        name="lugar_delete",
    ),

    path("posts/", views.PostListView.as_view(), name="post_list"),
    path("posts/nuevo/", views.PostCreateView.as_view(), name="post_create"),
    path("posts/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("posts/<int:pk>/editar/", views.PostUpdateView.as_view(), name="post_update"),
    path(
        "posts/<int:pk>/eliminar/",
        views.PostDeleteView.as_view(),
        name="post_delete",
    ),
]
