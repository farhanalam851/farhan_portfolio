"""Vercel entry point. Vercel's Python runtime looks for a WSGI callable named `app`."""
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.wsgi import get_wsgi_application  # noqa: E402

# Safety net: if the build step did not produce static files, make them once at cold start.
if not (BASE_DIR / "staticfiles").exists():
    from django.core.management import call_command
    try:
        call_command("collectstatic", interactive=False, verbosity=0)
    except Exception:
        pass

app = get_wsgi_application()
