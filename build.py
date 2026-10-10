"""Vercel build step: sets up the database. Vercel runs collectstatic itself.

Run as:  python build.py
Each step prints a clear header, so if the build fails the log shows exactly which step and why.
"""
import os
import subprocess
import sys
from urllib.parse import urlparse


def run(label, *args, required=True):
    print(f"\n==> {label}", flush=True)
    result = subprocess.run([sys.executable, "manage.py", *args])
    if result.returncode != 0:
        if required:
            print(f"\nBUILD FAILED at step: {label} (exit code {result.returncode}).", flush=True)
            print("Read the error printed just above this line.", flush=True)
            sys.exit(result.returncode)
        print(f"(step '{label}' did not succeed; continuing)", flush=True)


def main():
    print(f"Python: {sys.executable} {sys.version.split()[0]}", flush=True)
    try:
        import django
        print(f"Django: {django.get_version()}", flush=True)
    except ImportError:
        print("BUILD FAILED: Django is not installed. Check that requirements.txt is in the project root.")
        sys.exit(1)

    db_url = os.environ.get("DATABASE_URL") or os.environ.get("POSTGRES_URL") or ""
    if not db_url:
        print("\nWARNING: no DATABASE_URL or POSTGRES_URL is set, so the database was NOT set up.")
        print("Add a Neon Postgres database under Vercel > Storage, connect it to this project, then redeploy.")
        return

    parsed = urlparse(db_url)
    print(f"Database: {parsed.scheme} on host {parsed.hostname}", flush=True)

    run("Apply database migrations", "migrate", "--noinput")
    run("Load starter content", "seed_content")
    if os.environ.get("DJANGO_SUPERUSER_USERNAME") and os.environ.get("DJANGO_SUPERUSER_PASSWORD"):
        # Fails harmlessly if the admin already exists.
        run("Create admin login", "createsuperuser", "--noinput", required=False)
    else:
        print("\nSkipping admin creation: set DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD to create one.")
    print("\nBuild step finished.")


if __name__ == "__main__":
    main()
