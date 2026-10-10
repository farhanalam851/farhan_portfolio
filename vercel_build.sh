#!/usr/bin/env bash
# Build step for Vercel. Runs once per deployment, after dependencies are installed.
# Vercel runs collectstatic by itself and serves /static/ from its CDN, so it is not called here.
set -o errexit

# Database setup. Needs DATABASE_URL (or POSTGRES_URL) in Vercel's Environment Variables.
if [[ -n "${DATABASE_URL:-}${POSTGRES_URL:-}" ]]; then
  python3 manage.py migrate --noinput
  python3 manage.py seed_content
  if [[ -n "${DJANGO_SUPERUSER_USERNAME:-}" ]]; then
    python3 manage.py createsuperuser --noinput || true   # harmless if it already exists
  fi
else
  echo "WARNING: no DATABASE_URL set, skipping migrate/seed. The site will not work until you add one."
fi
