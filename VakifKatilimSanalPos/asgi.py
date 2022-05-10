"""
ASGI config for VakifKatilimSanalPos project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.VakifKatilimSanalPos.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'VakifKatilimSanalPos.settings')

application = get_asgi_application()
