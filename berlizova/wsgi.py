"""
WSGI config for the Berlizova project.

This module exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see:
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'berlizova' project
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "berlizova.settings")

# Get the WSGI application for the project
application = get_wsgi_application()
