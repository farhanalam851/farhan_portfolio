import os
import re
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.environ.get("DEBUG", "0" if os.environ.get("VERCEL") else "1") == "1"

SECRET_KEY = os.environ.get("SECRET_KEY", "")
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = "dev-only-insecure-key"
    else:
        from django.core.exceptions import ImproperlyConfigured
        raise ImproperlyConfigured("Set the SECRET_KEY environment variable when DEBUG=0.")

ALLOWED_HOSTS = [h.strip() for h in os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",") if h.strip()]
CSRF_TRUSTED_ORIGINS = [o.strip() for o in os.environ.get("CSRF_TRUSTED_ORIGINS", "").split(",") if o.strip()]

# Hosts that tell the app their own public address (Render, Railway, Vercel).
for _host in (
    os.environ.get("RENDER_EXTERNAL_HOSTNAME"),
    os.environ.get("RAILWAY_PUBLIC_DOMAIN"),
    os.environ.get("VERCEL_URL"),                      # this deployment's own URL
    os.environ.get("VERCEL_BRANCH_URL"),               # branch preview URL
    os.environ.get("VERCEL_PROJECT_PRODUCTION_URL"),   # your production *.vercel.app URL
):
    if _host:
        ALLOWED_HOSTS.append(_host)
        CSRF_TRUSTED_ORIGINS.append(f"https://{_host}")

ON_VERCEL = bool(os.environ.get("VERCEL"))
if ON_VERCEL:
    ALLOWED_HOSTS.append(".vercel.app")

# Every real (non-wildcard) allowed host is also a trusted origin for form posts, so adding a custom
# domain to ALLOWED_HOSTS is enough. Without this, the contact form fails with "CSRF verification failed".
for _h in ALLOWED_HOSTS:
    if _h and not _h.startswith(".") and _h not in ("localhost", "127.0.0.1", "*"):
        _origin = f"https://{_h}"
        if _origin not in CSRF_TRUSTED_ORIGINS:
            CSRF_TRUSTED_ORIGINS.append(_origin)

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# SQLite locally; set DATABASE_URL (e.g. postgres://...) in production.
# Vercel's Postgres/Neon integration may provide POSTGRES_URL instead of DATABASE_URL.
_db_url = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL") or ""
DATABASES = {
    "default": dj_database_url.parse(
        _db_url or f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        # Serverless functions should not hold connections open between requests.
        conn_max_age=0 if ON_VERCEL else 600,
    )
}
# Neon and most hosted Postgres refuse connections without SSL.
if _db_url and not _db_url.startswith("sqlite") and not DEBUG:
    DATABASES["default"].setdefault("OPTIONS", {}).setdefault("sslmode", "require")

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
# Files in static/root/ (favicon.ico, apple-touch-icon.png) are served at the site root,
# because browsers and phones request them at /favicon.ico and /apple-touch-icon.png.
WHITENOISE_ROOT = BASE_DIR / "static" / "root"
if os.environ.get("VERCEL"):
    # Vercel's CDN serves /static/ directly, and the function has no manifest file to read.
    _static_backend = "django.contrib.staticfiles.storage.StaticFilesStorage"
elif DEBUG:
    _static_backend = "whitenoise.storage.CompressedStaticFilesStorage"
else:
    _static_backend = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": _static_backend},
}

CSRF_FAILURE_VIEW = "core.views.csrf_failed"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Optional: set these to receive an email for every contact message.
EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = os.environ.get("EMAIL_HOST", "")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "587"))
EMAIL_USE_TLS = True
EMAIL_TIMEOUT = 10  # seconds; stops a slow mail server from hanging the page
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
CONTACT_NOTIFY_EMAIL = "farhanalam8510@gmail.com"

# Google Analytics 4 Measurement ID, e.g. G-ABC123XYZ. Leave empty to disable analytics.
# The tracking script only loads after the visitor accepts the cookie banner.
_ga = os.environ.get("GA_MEASUREMENT_ID", "").strip()
GA_MEASUREMENT_ID = _ga if re.fullmatch(r"G-[A-Z0-9]{4,20}", _ga) else ""

# Shown on the privacy policy and terms pages. Update when you change those pages.
LEGAL_LAST_UPDATED = "10 October 2026"

if not DEBUG:
    SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "1") == "1"
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", "3600"))  # raise to 31536000 once stable
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"
