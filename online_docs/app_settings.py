"""Settings for the ``django-online-docs`` app."""
from django.conf import settings


DOCS_DEBUG = getattr(settings, 'ONLINE_DOCS_DEBUG', False)
