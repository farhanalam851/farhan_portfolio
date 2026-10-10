# Deploying the portfolio

Free-plan details change often, so check each host's current pricing page before you pick one.

## Before you deploy (do this on your computer)

1. Run the site locally once (see README.md) and click through every section on a phone-sized window.
2. Add your real photos to `static/img/` if you want different ones, and check the resume PDF in `static/files/`.
3. Run Django's own deployment check and fix anything it flags:
   ```bash
   DEBUG=0 SECRET_KEY=test python manage.py check --deploy      # macOS/Linux
   set DEBUG=0 && set SECRET_KEY=test && python manage.py check --deploy    # Windows
   ```
4. Put the project on GitHub (the `.gitignore` already keeps secrets and the local database out):
   ```bash
   git init && git add . && git commit -m "Portfolio"
   ```
   Then create a repository on GitHub and push to it.

## Option 0: Vercel

Vercel runs Django as a serverless function, so two things differ from a normal host:
**SQLite will not work** (the filesystem is read-only and resets), so you need a hosted Postgres,
and your database is set up during the build rather than at startup. The repo already contains
`vercel.json`, `api/index.py` and `vercel_build.sh` for this.

1. Push the project to GitHub (see above).
2. On vercel.com choose **Add New > Project**, import the repo, and leave Framework Preset as **Other**.
3. Before deploying, open the project's **Storage** tab (or Marketplace) and add a **Neon Postgres**
   database. Connect it to the project. This adds `DATABASE_URL` automatically.
4. In **Settings > Environment Variables** add:
   - `DEBUG` = `0`
   - `SECRET_KEY` = a long random string (`python -c "import secrets;print(secrets.token_urlsafe(50))"`)
   - `DJANGO_SUPERUSER_USERNAME` = `farhan`
   - `DJANGO_SUPERUSER_EMAIL` = `farhanalam8510@gmail.com`
   - `DJANGO_SUPERUSER_PASSWORD` = a strong password
   - optional: `EMAIL_*` and `GA_MEASUREMENT_ID` (see `.env.example`)
5. Click **Deploy**. `vercel_build.sh` collects static files, migrates the database, loads your starter
   content and creates your admin login. Open the `*.vercel.app` address, then `/admin/`.
6. Custom domain: add it under **Settings > Domains**, then add it to `ALLOWED_HOSTS` and
   `CSRF_TRUSTED_ORIGINS` (with `https://`) as environment variables and redeploy.

Notes: the `*.vercel.app` hostnames are allowed automatically. Remove `DJANGO_SUPERUSER_PASSWORD`
from Vercel once your admin account exists if you prefer. Content edits made in `/admin/` live in the
database, so they survive redeploys.

## Option A: Render (blueprint included)

1. Sign in at render.com with GitHub, choose **New > Blueprint**, and pick your repository.
2. Render reads `render.yaml` and creates the web service and a Postgres database.
3. When prompted, enter `DJANGO_SUPERUSER_PASSWORD` (a strong password). Your admin username is `farhan`.
4. Wait for the build. `build.sh` installs packages, collects static files, migrates the database,
   loads your starter content and creates your admin login.
5. Open the `onrender.com` address, then `/admin/` to sign in.

Things to know: free web services on Render may sleep after a period without visits, so the first load
can be slow, which is not ideal when a recruiter clicks your link. Free databases may also expire.
Check Render's current terms, and consider a small paid plan once you are sharing the link widely.

## Option B: Railway

1. New Project > Deploy from GitHub repo. Add a Postgres database to the project.
2. In the web service's Variables, set `DEBUG=0`, `SECRET_KEY`, and `DATABASE_URL` (reference the Postgres variable).
   Also set the `DJANGO_SUPERUSER_*` variables.
3. Set the build command to `bash build.sh` and the start command to the one in `Procfile`.
4. Generate a public domain in Settings > Networking.

## Option C: PythonAnywhere

Good if you want SQLite to simply persist without a separate database. Upload or clone the project, create a
virtualenv, `pip install -r requirements.txt`, then run `migrate`, `seed_content`, `createsuperuser` and
`collectstatic` in a console. Point the web app's WSGI file at `config.wsgi` and map `/static/` to the
`staticfiles` folder. Set the environment variables in the WSGI file.

## Your own domain

Buy a domain (for example farhanalam.dev), add it in your host's Custom Domains screen, create the DNS records
the host shows you, then add the domain to `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` (with `https://`).

## After it is live

- Sign in to `/admin/`, open **Site profile** and confirm your links, email and numbers.
- Submit the contact form once yourself, then check **Contact messages**. Set the EMAIL_* variables (see
  `.env.example`) if you also want enquiries in your inbox.
- Add the live URL to your GitHub profile, LinkedIn, resume and the Instagram bio link.
- Share the link in a private window or on your phone to see what a recruiter sees.

## Search and sharing setup (after the site is live)

- **Google Search Console:** add your domain, then submit `https://yourdomain/sitemap.xml`.
- **Share previews:** paste your link into WhatsApp or LinkedIn's Post Inspector (linkedin.com/post-inspector) to confirm
  the image and title appear. They cache old previews, so use the inspector to refresh after changes.
- **Analytics:** add the `GA_MEASUREMENT_ID` environment variable (see README) and redeploy.
- **Legal pages:** read `/privacy/` and `/terms/` once, edit anything that does not match how you work, and ideally
  have someone with legal knowledge review them.

## Security reminders

- Never commit `.env` or passwords. `.env.example` has placeholders only.
- Use a long random `SECRET_KEY` and a unique, strong admin password.
- Once everything works over HTTPS, raise `SECURE_HSTS_SECONDS` to `31536000`.
