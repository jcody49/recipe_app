"""
WSGI config for recipe_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from pathlib import Path  
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recipe_project.settings')

application = get_wsgi_application()
application = WhiteNoise(application, root=Path(__file__).resolve(strict=True).parent.parent  / 'staticfiles')
application.add_files(Path(__file__).resolve(strict=True).parent.parent / 'media', prefix='media/')
