"""
Pruebas básicas de la app blog.

Cubren: creación de modelos, vistas de listado/detalle, búsqueda,
protección por login y flujo de registro.
"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Lugar, Post, TipoLugar


class ModeloTests(TestCase):
    def test_str_y_slug(self):
        tipo = TipoLugar.objects.create(nombre="Glaciar")
        lugar = Lugar.objects.create(
            nombre="Glaciar Perito Moreno",
            provincia="santa_cruz",
            tipo=tipo,
            descripcion="Imponente glaciar en Santa Cruz.",
        )
        self.assertEqual(str(tipo), "Glaciar")
        self.assertEqual(lugar.slug, "glaciar-perito-moreno")
        self.assertIn("Santa Cruz", str(lugar))


class VistasTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ana", password="clave12345")
        self.tipo = TipoLugar.objects.create(nombre="Ciudad")
        self.lugar = Lugar.objects.create(
            nombre="Bariloche",
            provincia="rio_negro",
            tipo=self.tipo,
            descripcion="Ciudad de montaña y lagos.",
        )
        self.post = Post.objects.create(
            titulo="Fin de semana en Bariloche",
            contenido="Chocolate, lagos y cerros.",
            lugar=self.lugar,
            autor=self.user,
        )

    def test_home_ok(self):
        self.assertEqual(self.client.get(reverse("home")).status_code, 200)

    def test_about_ok(self):
        self.assertEqual(self.client.get(reverse("about")).status_code, 200)

    def test_busqueda_lugares(self):
        resp = self.client.get(reverse("lugar_list"), {"q": "Bariloche"})
        self.assertContains(resp, "Bariloche")
        resp_vacio = self.client.get(reverse("lugar_list"), {"q": "Tokio"})
        self.assertNotContains(resp_vacio, "Bariloche")

    def test_busqueda_posts(self):
        resp = self.client.get(reverse("post_list"), {"q": "chocolate"})
        self.assertContains(resp, "Bariloche")

    def test_crear_post_requiere_login(self):
        resp = self.client.get(reverse("post_create"))
        self.assertEqual(resp.status_code, 302)
        self.assertIn("/login/", resp.url)

    def test_crear_post_logueado(self):
        self.client.login(username="ana", password="clave12345")
        resp = self.client.post(
            reverse("post_create"),
            {
                "titulo": "Viaje a El Chaltén",
                "lugar": self.lugar.pk,
                "contenido": "Trekking al Fitz Roy.",
                "publicado": True,
            },
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Post.objects.filter(titulo="Viaje a El Chaltén").exists())

    def test_registro(self):
        resp = self.client.post(
            reverse("register"),
            {
                "username": "nuevo",
                "email": "nuevo@example.com",
                "password1": "ClaveSegura2026",
                "password2": "ClaveSegura2026",
            },
        )
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(User.objects.filter(username="nuevo").exists())
