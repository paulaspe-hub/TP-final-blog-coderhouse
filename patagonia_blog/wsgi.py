"""
Configuración WSGI para el proyecto patagonia_blog.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "patagonia_blog.settings")

application = get_wsgi_application()
