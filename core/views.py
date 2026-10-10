import json
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.templatetags.static import static

from .content import get_content, get_profile
from .forms import ContactForm

logger = logging.getLogger(__name__)


def _schema(request, p):
    """JSON-LD so Google can show a rich result for the person."""
    base = f"{request.scheme}://{request.get_host()}"
    doc = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": p["name"],
        "url": f"{base}/",
        "image": f"{base}{static('img/og-image.jpg')}",
        "jobTitle": "Full Stack Web Developer",
        "email": p["email"],
        "address": {"@type": "PostalAddress", "addressLocality": "Kanpur",
                    "addressRegion": "Uttar Pradesh", "addressCountry": "IN"},
        "sameAs": [p["github"], p["linkedin"], p["instagram"]],
        "knowsAbout": ["Python", "Django", "Django REST Framework", "JavaScript", "HTML", "CSS",
                       "Bootstrap", "PostgreSQL", "Web development"],
    }
    # "<" is escaped so the JSON can never close the script tag early.
    return json.dumps(doc).replace("<", "\\u003c")


def home(request):
    if request.method == "POST":
        # Bots fill the hidden honeypot field. Pretend it worked, save nothing.
        if request.POST.get("contact_hp"):
            return redirect("thanks")
        form = ContactForm(request.POST)
        if form.is_valid():
            try:
                msg = form.save()
            except Exception:
                # Most likely the database is unreachable or not migrated. Log it (visible in
                # Vercel > Logs) and tell the visitor how to reach me instead of showing a 500.
                logger.exception("Contact form: could not save message")
                form.add_error(None, "Sorry, your message could not be saved just now. "
                                     f"Please email me directly at {settings.CONTACT_NOTIFY_EMAIL}.")
            else:
                try:
                    send_mail(
                        subject=f"Portfolio enquiry: {msg.get_topic_display()} from {msg.name}",
                        message=f"From: {msg.name} <{msg.email}>\n\n{msg.message}",
                        from_email=settings.EMAIL_HOST_USER or settings.CONTACT_NOTIFY_EMAIL,
                        recipient_list=[settings.CONTACT_NOTIFY_EMAIL],
                        fail_silently=True,
                    )
                except Exception:
                    logger.exception("Contact form: notification email failed")
                request.session["contact_sent"] = True  # lets the thank-you page count one real enquiry
                return redirect("thanks")
    else:
        form = ContactForm()

    p = get_profile(request)
    context = {"focus": p["focus"], "form": form, "schema_json": _schema(request, p), **get_content()}
    return render(request, "core/home.html", context)


def thanks(request):
    just_sent = request.session.pop("contact_sent", False)
    return render(request, "core/thanks.html", {"just_sent": just_sent})


def privacy(request):
    return render(request, "core/privacy.html")


def terms(request):
    return render(request, "core/terms.html")


def csrf_failed(request, reason=""):
    """A readable message instead of Django's bare 403 when the form's security token is stale."""
    from django.http import HttpResponse
    logger.warning("CSRF failure: %s (host=%s, origin=%s)", reason,
                   request.get_host(), request.META.get("HTTP_ORIGIN"))
    return HttpResponse(
        "<!doctype html><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'>"
        "<title>Please try again</title><body style='font-family:system-ui;max-width:32rem;margin:4rem auto;padding:0 1rem'>"
        "<h1>Please try again</h1><p>Your form expired before it was sent. "
        "Go back, reload the page, and send it again.</p>"
        f"<p>Or email me directly at <a href='mailto:{settings.CONTACT_NOTIFY_EMAIL}'>{settings.CONTACT_NOTIFY_EMAIL}</a>.</p>"
        "<p><a href='/#contact'>Back to the form</a></p>",
        status=403,
    )
