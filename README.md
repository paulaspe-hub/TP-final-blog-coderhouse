# Patagonia Blog

Blog de **lugares turísticos de la Patagonia Argentina** desarrollado con **Django** y **SQLite**.
Incluye CRUD completo de 3 modelos, búsqueda con formularios HTML, página `/about` y autenticación
(registro / login / logout).

---

## Stack y decisiones

- **Django** (ver `requirements.txt`) + **SQLite** (config estándar).
- **Estrategia de vistas: Class-Based Views (CBV)** usadas de forma consistente en todo el CRUD
  (`ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView`).
- Las vistas de **crear / editar / eliminar** están protegidas con `LoginRequiredMixin`.
- Mensajes al usuario con `django.contrib.messages` (integrados con Bootstrap).
- UI con **Bootstrap 5** vía CDN y herencia de templates desde `base.html`.

---

## Orden exacto para probar todo (paso a paso)

Desde la carpeta raíz del proyecto (`blog-python/`), en una terminal de Windows (PowerShell):

```powershell
# 1) Crear y activar el entorno virtual
python -m venv venv
venv\Scripts\activate

# 2) Instalar dependencias
pip install -r requirements.txt

# 3) Crear las migraciones y aplicarlas (genera db.sqlite3)
python manage.py makemigrations
python manage.py migrate

# 4) (Opcional) Cargar datos de ejemplo de la Patagonia
python manage.py loaddata sample_data

# 5) (Opcional pero recomendado) Crear un superusuario para el admin
python manage.py createsuperuser

# 6) Levantar el servidor de desarrollo
python manage.py runserver
```

> En Linux/macOS, activá el venv con `source venv/bin/activate`.

Luego abrí el navegador en **http://127.0.0.1:8000/**.

### Cómo probar cada funcionalidad

1. **Home:** http://127.0.0.1:8000/ — muestra estadísticas y últimos posts.
2. **About:** http://127.0.0.1:8000/about/ — página "Acerca de mí" (también enlazada en el navbar).
3. **Registro:** http://127.0.0.1:8000/register/ — creá una cuenta (te loguea automáticamente).
4. **Login / Logout:** http://127.0.0.1:8000/login/ y botón **Salir** del navbar.
5. **CRUD Tipos de lugar:** http://127.0.0.1:8000/tipos/ (botones Nuevo/Editar/Eliminar visibles si estás logueado).
6. **CRUD Lugares:** http://127.0.0.1:8000/lugares/ — incluye **búsqueda** por nombre, provincia y tipo.
7. **CRUD Posts:** http://127.0.0.1:8000/posts/ — incluye **búsqueda** por título/contenido y filtro por lugar.
8. **Protección por login:** sin estar logueado, entrar a http://127.0.0.1:8000/posts/nuevo/ te redirige al login.

### Correr los tests

```powershell
python manage.py test
```

---

## Dónde está implementada cada funcionalidad

| Funcionalidad | Archivo(s) |
|---|---|
| **Configuración / INSTALLED_APPS / DB SQLite** | `patagonia_blog/settings.py` |
| **URLs principales** (enlaza app y auth) | `patagonia_blog/urls.py` |
| **Modelos** (TipoLugar, Lugar, Post) | `blog/models.py` |
| **Formularios + validaciones** | `blog/forms.py` |
| **Vistas CRUD (CBV)** | `blog/views.py` |
| **URLs de la app** (home, about, CRUD) | `blog/urls.py` |
| **URLs de autenticación** | `blog/auth_urls.py` |
| **Admin** | `blog/admin.py` |
| **Template base + navbar** | `blog/templates/base.html` |
| **Home / About** | `blog/templates/blog/home.html`, `about.html` |
| **Templates CRUD** | `blog/templates/blog/{tipolugar,lugar,post}_*.html` |
| **Templates de auth** | `blog/templates/registration/login.html`, `register.html` |
| **Búsqueda (ORM)** | `LugarListView` y `PostListView` en `blog/views.py` |
| **Datos de ejemplo** | `blog/fixtures/sample_data.json` |
| **Tests** | `blog/tests.py` |

---

## Modelos (`blog/models.py`)

- **`TipoLugar`** — categoría de lugar (ej: Glaciar, Parque Nacional). Campos: `nombre`, `slug`, `descripcion`.
- **`Lugar`** — lugar turístico. Campos: `nombre`, `slug`, `provincia` (choices de provincias patagónicas),
  `descripcion`, `mejor_epoca`, `creado` + **FK** a `TipoLugar`.
- **`Post`** — artículo del blog. Campos: `titulo`, `slug`, `contenido`, `publicado`, `creado`, `actualizado`
  + **FK** a `Lugar` y **FK** al `User` autor.

Relaciones: `Lugar → TipoLugar` (FK) y `Post → Lugar` / `Post → User` (FK). Todos tienen `__str__`.

---

## Mapa de rutas / endpoints

| Método | URL | Vista | Descripción |
|---|---|---|---|
| GET | `/` | `HomeView` | Inicio con estadísticas y últimos posts |
| GET | `/about/` | `AboutView` | Página "Acerca de mí" |
| GET | `/tipos/` | `TipoLugarListView` | Listado + búsqueda de tipos |
| GET/POST | `/tipos/nuevo/` | `TipoLugarCreateView` | Crear tipo (login) |
| GET/POST | `/tipos/<pk>/editar/` | `TipoLugarUpdateView` | Editar tipo (login) |
| GET/POST | `/tipos/<pk>/eliminar/` | `TipoLugarDeleteView` | Eliminar tipo con confirmación (login) |
| GET | `/lugares/` | `LugarListView` | Listado + **búsqueda** (nombre/provincia/tipo) |
| GET | `/lugares/<pk>/` | `LugarDetailView` | Detalle del lugar |
| GET/POST | `/lugares/nuevo/` | `LugarCreateView` | Crear lugar (login) |
| GET/POST | `/lugares/<pk>/editar/` | `LugarUpdateView` | Editar lugar (login) |
| GET/POST | `/lugares/<pk>/eliminar/` | `LugarDeleteView` | Eliminar lugar con confirmación (login) |
| GET | `/posts/` | `PostListView` | Listado + **búsqueda** (título/contenido/lugar) |
| GET | `/posts/<pk>/` | `PostDetailView` | Detalle del post |
| GET/POST | `/posts/nuevo/` | `PostCreateView` | Crear post (login) |
| GET/POST | `/posts/<pk>/editar/` | `PostUpdateView` | Editar post (login) |
| GET/POST | `/posts/<pk>/eliminar/` | `PostDeleteView` | Eliminar post con confirmación (login) |
| GET/POST | `/login/` | `LoginView` | Iniciar sesión |
| POST | `/logout/` | `LogoutView` | Cerrar sesión |
| GET/POST | `/register/` | `RegistroView` | Registrar usuario |
| — | `/admin/` | Django Admin | Panel de administración |

---

## Búsqueda

- **Lugares** (`/lugares/`): formulario HTML con campo de texto + selects de provincia y tipo.
  Consulta el ORM con `Q(nombre__icontains=...) | Q(descripcion__icontains=...)` y filtros por `provincia` y `tipo`.
- **Posts** (`/posts/`): formulario HTML por título/contenido y filtro por lugar.

---

## Autenticación

- Sistema de `django.contrib.auth`.
- Registro propio (`RegistroForm` basado en `UserCreationForm`).
- Templates propios en `blog/templates/registration/`.
- Secciones protegidas: crear/editar/eliminar de **todos** los modelos requieren login (`LoginRequiredMixin`).

---

## Árbol de archivos

```
blog-python/
├── .gitignore
├── README.md
├── requirements.txt
├── manage.py
├── db.sqlite3                # generado tras migrate (ignorado por git)
├── patagonia_blog/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── blog/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    ├── auth_urls.py
    ├── views.py
    ├── migrations/
    │   └── __init__.py
    ├── fixtures/
    │   └── sample_data.json
    └── templates/
        ├── base.html
        ├── registration/
        │   ├── login.html
        │   └── register.html
        └── blog/
            ├── home.html
            ├── about.html
            ├── _pagination.html
            ├── tipolugar_list.html
            ├── tipolugar_form.html
            ├── tipolugar_confirm_delete.html
            ├── lugar_list.html
            ├── lugar_detail.html
            ├── lugar_form.html
            ├── lugar_confirm_delete.html
            ├── post_list.html
            ├── post_detail.html
            ├── post_form.html
            └── post_confirm_delete.html
```
