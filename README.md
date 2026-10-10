# Farhan Alam: Portfolio (Django + Bootstrap 5)

## Run locally

```bash
python -m venv venv
venv\Scripts\activate          # Windows   (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_content      # loads your starting content into the admin panel
python manage.py createsuperuser   # your admin login
python manage.py runserver
```
Open http://127.0.0.1:8000

## Launch checklist: where each item lives

| Item | Where |
|---|---|
| Meta title and description per page | each page's `{% block seo %}` (home.html, privacy.html, terms.html, thanks.html, 404.html); defaults in `templates/partials/seo.html` |
| Open Graph / Twitter share image | `static/img/og-image.jpg` (1200x630) |
| Favicon set | `static/img/favicons/` plus `static/root/` (served at /favicon.ico and /apple-touch-icon.png) |
| robots.txt / sitemap.xml | `/robots.txt` (templates/robots.txt) and `/sitemap.xml` (`PortfolioSitemap` in core/urls.py) |
| Structured data (Google rich result) | JSON-LD built in `core/views.py` |
| Custom 404 / 500 pages | `templates/404.html`, `templates/500.html` (preview 404 locally at `/preview-404/`) |
| Thank-you page | `/thank-you/`, shown after the contact form is sent |
| Privacy policy / Terms | `core/templates/core/privacy.html`, `terms.html` (update the date in `LEGAL_LAST_UPDATED`, config/settings.py) |
| Cookie banner | `templates/base.html` + `static/js/analytics.js` |
| Analytics | set `GA_MEASUREMENT_ID` (see below) |
| Sticky mobile CTA, form validation, loading states | `static/js/forms.js`, styles at the end of `static/css/style.css` |

### Turning analytics on

1. In Google Analytics create a GA4 property and copy the Measurement ID (`G-XXXXXXXXXX`).
2. Set it as the `GA_MEASUREMENT_ID` environment variable (locally: `set GA_MEASUREMENT_ID=G-XXXXXXXXXX` on Windows,
   `export GA_MEASUREMENT_ID=...` on macOS/Linux).
3. Visitors who click **Accept analytics** are tracked. Events sent: clicks on the main buttons (`cta_start_project`,
   `cta_see_work`, `resume_download`, `nav_hire_me`, mobile bar buttons) and `generate_lead` when a real enquiry is sent.
   In GA4, mark `generate_lead` as a key event to count enquiries as conversions.

### Tests

```bash
python manage.py test
```
Run it with `DEBUG` unset. It checks every page, SEO tags, alt text, robots/sitemap, the 404, the form, and analytics gating.

## Admin panel

Open http://127.0.0.1:8000/admin/ and sign in with the superuser you created.

- **Projects, Skills, Services, Journey items**: add, edit, reorder (change the *Order* number) or hide
  (untick *Is visible*) with no code changes. Changes show on the site immediately.
- **Contact messages**: every enquiry from the form lands here. Tick *Is read* once handled.
- Until you run `seed_content`, the site shows the starter content from `core/data.py`.
  Use `python manage.py seed_content --force` to wipe and reload that starter content.
- **Site profile**: your name, email, links, typing role lines, About focus list and the three hero numbers.
  (One record only; edit it, don't add another.)
- **Moving logos**: add or reorder the logos in the top and bottom strips.
- **Process steps**: the Talk / Plan / Build / Launch steps (numbered automatically by order).
- In production, run `seed_content` and `createsuperuser` once on the server, and use a strong password.

## Where to edit things

| What | File |
|---|---|
| Starter content (only used until you run `seed_content`; after that use /admin/) | `core/data.py` |
| Layout and sections | `core/templates/core/home.html` |
| Colours, fonts, animations | `static/css/style.css` (tokens at the top) |
| JS effects (typing, tilt, theme, reveal) | `static/js/main.js` |
| Photos | `static/img/` (hero.jpg, about.jpg, gallery-1.jpg, gallery-2.jpg) |
| Resume download | `static/files/Farhan_Alam_Resume.pdf` |

Contact form messages are saved in the database (view them in `/admin/`) and also emailed to the
address in `CONTACT_NOTIFY_EMAIL` if you set the EMAIL_* environment variables.

## Deploy

See **DEPLOY.md** for step-by-step Render, Railway and PythonAnywhere instructions. Quick summary:

Environment variables: `DEBUG=0`, `SECRET_KEY=<long random string>`, `ALLOWED_HOSTS=yourdomain.com`,
`CSRF_TRUSTED_ORIGINS=https://yourdomain.com`, `DATABASE_URL=<postgres url>`.

```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn config.wsgi
```
