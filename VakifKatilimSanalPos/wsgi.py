"""
WSGI config for VakifKatilimSanalPos project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.VakifKatilimSanalPos.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VakifKatilimSanalPos.settings')

application = get_wsgi_application()
