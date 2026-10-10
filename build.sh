#!/usr/bin/env bash
# Build step for Render / Railway / similar hosts.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
python manage.py seed_content

# Creates your admin login on first deploy (needs DJANGO_SUPERUSER_* env vars). Harmless if it already exists.
if [[ -n "${DJANGO_SUPERUSER_USERNAME:-}" ]]; then
  python manage.py createsuperuser --noinput || true
fi
