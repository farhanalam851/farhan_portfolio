from django.conf import settings

from .content import get_profile


def site(request):
    """Variables available in every template (including 404)."""
    return {
        "p": get_profile(request),
        "GA_ID": settings.GA_MEASUREMENT_ID,
        "LEGAL_UPDATED": settings.LEGAL_LAST_UPDATED,
    }
