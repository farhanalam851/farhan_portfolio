from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from . import data
from .forms import ContactForm


def home(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save()
            try:
                send_mail(
                    subject=f"Portfolio enquiry: {msg.get_topic_display()} from {msg.name}",
                    message=f"From: {msg.name} <{msg.email}>\n\n{msg.message}",
                    from_email=settings.EMAIL_HOST_USER or settings.CONTACT_NOTIFY_EMAIL,
                    recipient_list=[settings.CONTACT_NOTIFY_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            messages.success(request, "Thanks! Your message is in. I'll reply within a day.")
            return redirect("/#contact")
        messages.error(request, "Please fix the highlighted fields and try again.")
    else:
        form = ContactForm()

    context = {
        "p": data.PROFILE,
        "logos_1": data.LOGOS_ROW_1,
        "logos_2": data.LOGOS_ROW_2,
        "skills": data.SKILLS,
        "projects": data.PROJECTS,
        "services": data.SERVICES,
        "process": data.PROCESS,
        "journey": data.JOURNEY,
        "focus": data.FOCUS,
        "form": form,
    }
    return render(request, "core/home.html", context)
