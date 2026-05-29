"""
Formularios de la app blog.

Incluye:
- ModelForms para los tres modelos (con validaciones básicas).
- Formulario de registro de usuarios.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Lugar, Post, TipoLugar


class TipoLugarForm(forms.ModelForm):
    class Meta:
        model = TipoLugar
        fields = ["nombre", "descripcion"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre


class LugarForm(forms.ModelForm):
    class Meta:
        model = Lugar
        fields = ["nombre", "provincia", "tipo", "descripcion", "mejor_epoca"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "provincia": forms.Select(attrs={"class": "form-select"}),
            "tipo": forms.Select(attrs={"class": "form-select"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "mejor_epoca": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()
        if len(nombre) < 3:
            raise forms.ValidationError("El nombre debe tener al menos 3 caracteres.")
        return nombre


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["titulo", "lugar", "contenido", "publicado"]
        widgets = {
            "titulo": forms.TextInput(attrs={"class": "form-control"}),
            "lugar": forms.Select(attrs={"class": "form-select"}),
            "contenido": forms.Textarea(attrs={"class": "form-control", "rows": 8}),
            "publicado": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_titulo(self):
        titulo = self.cleaned_data["titulo"].strip()
        if len(titulo) < 5:
            raise forms.ValidationError("El título debe tener al menos 5 caracteres.")
        return titulo


class RegistroForm(UserCreationForm):
    """Formulario de registro basado en el sistema de auth de Django."""

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
