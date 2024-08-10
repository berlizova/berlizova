"""
ASGI config for the Berlizova project.

This file exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see:
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set the default Django settings module for the 'asgi' application.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "berlizova.settings")

# Get the ASGI application callable.
application = get_asgi_application()
