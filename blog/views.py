"""
Vistas de la app blog.

Estrategia elegida: Class-Based Views (CBV) de forma consistente.
- CRUD de los 3 modelos con ListView / DetailView / CreateView / UpdateView / DeleteView.
- Las vistas de creación, edición y borrado están protegidas con LoginRequiredMixin.
- Búsqueda HTML implementada en las ListView de Lugar y Post mediante el ORM.
"""

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import LugarForm, PostForm, RegistroForm, TipoLugarForm
from .models import Lugar, Post, TipoLugar


class HomeView(TemplateView):
    template_name = "blog/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["ultimos_posts"] = Post.objects.filter(publicado=True)[:5]
        ctx["total_lugares"] = Lugar.objects.count()
        ctx["total_posts"] = Post.objects.count()
        ctx["total_tipos"] = TipoLugar.objects.count()
        return ctx


class AboutView(TemplateView):
    template_name = "blog/about.html"


class TipoLugarListView(ListView):
    model = TipoLugar
    template_name = "blog/tipolugar_list.html"
    context_object_name = "tipos"

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        return ctx


class TipoLugarCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = TipoLugar
    form_class = TipoLugarForm
    template_name = "blog/tipolugar_form.html"
    success_url = reverse_lazy("tipolugar_list")
    success_message = "Tipo de lugar creado correctamente."


class TipoLugarUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = TipoLugar
    form_class = TipoLugarForm
    template_name = "blog/tipolugar_form.html"
    success_url = reverse_lazy("tipolugar_list")
    success_message = "Tipo de lugar actualizado correctamente."


class TipoLugarDeleteView(LoginRequiredMixin, DeleteView):
    model = TipoLugar
    template_name = "blog/tipolugar_confirm_delete.html"
    success_url = reverse_lazy("tipolugar_list")

    def form_valid(self, form):
        messages.success(self.request, "Tipo de lugar eliminado correctamente.")
        return super().form_valid(form)


class LugarListView(ListView):
    model = Lugar
    template_name = "blog/lugar_list.html"
    context_object_name = "lugares"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("tipo")
        q = self.request.GET.get("q", "").strip()
        provincia = self.request.GET.get("provincia", "").strip()
        tipo = self.request.GET.get("tipo", "").strip()
        if q:
            qs = qs.filter(Q(nombre__icontains=q) | Q(descripcion__icontains=q))
        if provincia:
            qs = qs.filter(provincia=provincia)
        if tipo:
            qs = qs.filter(tipo_id=tipo)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        from .models import PROVINCIAS

        ctx["q"] = self.request.GET.get("q", "")
        ctx["provincia_sel"] = self.request.GET.get("provincia", "")
        ctx["tipo_sel"] = self.request.GET.get("tipo", "")
        ctx["provincias"] = PROVINCIAS
        ctx["tipos"] = TipoLugar.objects.all()
        return ctx


class LugarDetailView(DetailView):
    model = Lugar
    template_name = "blog/lugar_detail.html"
    context_object_name = "lugar"


class LugarCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Lugar
    form_class = LugarForm
    template_name = "blog/lugar_form.html"
    success_message = "Lugar creado correctamente."


class LugarUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Lugar
    form_class = LugarForm
    template_name = "blog/lugar_form.html"
    success_message = "Lugar actualizado correctamente."


class LugarDeleteView(LoginRequiredMixin, DeleteView):
    model = Lugar
    template_name = "blog/lugar_confirm_delete.html"
    success_url = reverse_lazy("lugar_list")

    def form_valid(self, form):
        messages.success(self.request, "Lugar eliminado correctamente.")
        return super().form_valid(form)


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related("lugar", "autor")
        q = self.request.GET.get("q", "").strip()
        lugar = self.request.GET.get("lugar", "").strip()
        if q:
            qs = qs.filter(Q(titulo__icontains=q) | Q(contenido__icontains=q))
        if lugar:
            qs = qs.filter(lugar_id=lugar)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["q"] = self.request.GET.get("q", "")
        ctx["lugar_sel"] = self.request.GET.get("lugar", "")
        ctx["lugares"] = Lugar.objects.all()
        return ctx


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"


class PostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    success_message = "Post creado correctamente."

    def form_valid(self, form):
        form.instance.autor = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"
    success_message = "Post actualizado correctamente."


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post_list")

    def form_valid(self, form):
        messages.success(self.request, "Post eliminado correctamente.")
        return super().form_valid(form)


class RegistroView(CreateView):
    form_class = RegistroForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "¡Cuenta creada! Ya estás logueado.")
        return response
