from django.contrib import admin

from .models import Lugar, Post, TipoLugar


@admin.register(TipoLugar)
class TipoLugarAdmin(admin.ModelAdmin):
    list_display = ("nombre", "slug")
    search_fields = ("nombre",)
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(Lugar)
class LugarAdmin(admin.ModelAdmin):
    list_display = ("nombre", "provincia", "tipo", "creado")
    list_filter = ("provincia", "tipo")
    search_fields = ("nombre", "descripcion")
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("titulo", "lugar", "autor", "publicado", "creado")
    list_filter = ("publicado", "lugar")
    search_fields = ("titulo", "contenido")
    prepopulated_fields = {"slug": ("titulo",)}
