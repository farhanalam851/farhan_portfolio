# Farhan Alam: Portfolio (Django + Bootstrap 5)

## Run locally

```bash
python -m venv venv
venv\Scripts\activate          # Windows   (macOS/Linux: source venv/bin/activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # to read contact messages at /admin/
python manage.py runserver
```
Open http://127.0.0.1:8000

## Where to edit things

| What | File |
|---|---|
| Name, links, roles, skills, projects, services, timeline | `core/data.py` |
| Layout and sections | `core/templates/core/home.html` |
| Colours, fonts, animations | `static/css/style.css` (tokens at the top) |
| JS effects (typing, tilt, theme, reveal) | `static/js/main.js` |
| Photos | `static/img/` (hero.jpg, about.jpg, gallery-1.jpg, gallery-2.jpg) |
| Resume download | `static/files/Farhan_Alam_Resume.pdf` |

Contact form messages are saved in the database (view them in `/admin/`) and also emailed to the
address in `CONTACT_NOTIFY_EMAIL` if you set the EMAIL_* environment variables.

## Deploy (Render / Railway / any host)

Environment variables: `DEBUG=0`, `SECRET_KEY=<long random string>`, `ALLOWED_HOSTS=yourdomain.com`,
`CSRF_TRUSTED_ORIGINS=https://yourdomain.com`, `DATABASE_URL=<postgres url>`.

```bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
gunicorn config.wsgi
```
