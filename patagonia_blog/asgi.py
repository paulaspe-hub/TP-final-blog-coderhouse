"""
Configuración ASGI para el proyecto patagonia_blog.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "patagonia_blog.settings")

application = get_asgi_application()
