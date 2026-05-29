"""
Modelos del blog turístico de la Patagonia Argentina.

Tres modelos principales con relaciones:
- TipoLugar: categoría/tipo de lugar (ej: Parque Nacional, Glaciar, Ciudad).
- Lugar: lugar turístico concreto (FK a TipoLugar).
- Post: artículo del blog sobre un lugar (FK a Lugar y FK al autor/User).
"""

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


# Provincias de la Patagonia Argentina
PROVINCIAS = [
    ("neuquen", "Neuquén"),
    ("rio_negro", "Río Negro"),
    ("chubut", "Chubut"),
    ("santa_cruz", "Santa Cruz"),
    ("tierra_del_fuego", "Tierra del Fuego"),
    ("la_pampa", "La Pampa"),
]


class TipoLugar(models.Model):

    nombre = models.CharField("Nombre", max_length=80, unique=True)
    slug = models.SlugField("Slug", max_length=90, unique=True, blank=True)
    descripcion = models.TextField("Descripción", blank=True)

    class Meta:
        verbose_name = "Tipo de lugar"
        verbose_name_plural = "Tipos de lugar"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("tipolugar_list")


class Lugar(models.Model):

    nombre = models.CharField("Nombre", max_length=150)
    slug = models.SlugField("Slug", max_length=170, unique=True, blank=True)
    provincia = models.CharField("Provincia", max_length=30, choices=PROVINCIAS)
    tipo = models.ForeignKey(
        TipoLugar,
        on_delete=models.PROTECT,
        related_name="lugares",
        verbose_name="Tipo de lugar",
    )
    descripcion = models.TextField("Descripción")
    mejor_epoca = models.CharField(
        "Mejor época para visitar", max_length=120, blank=True
    )
    creado = models.DateTimeField("Creado", auto_now_add=True)

    class Meta:
        verbose_name = "Lugar"
        verbose_name_plural = "Lugares"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.get_provincia_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("lugar_detail", kwargs={"pk": self.pk})


class Post(models.Model):

    titulo = models.CharField("Título", max_length=200)
    slug = models.SlugField("Slug", max_length=220, unique=True, blank=True)
    contenido = models.TextField("Contenido")
    lugar = models.ForeignKey(
        Lugar,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Lugar",
    )
    autor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
        verbose_name="Autor",
    )
    publicado = models.BooleanField("Publicado", default=True)
    creado = models.DateTimeField("Creado", auto_now_add=True)
    actualizado = models.DateTimeField("Actualizado", auto_now=True)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-creado"]

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})
