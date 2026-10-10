from django.contrib.sitemaps import Sitemap
from django.contrib.sitemaps.views import sitemap
from django.http import Http404
from django.urls import path
from django.views.defaults import page_not_found
from django.views.generic import RedirectView, TemplateView

from . import views


class PortfolioSitemap(Sitemap):
    """Public pages only. The thank-you page is deliberately left out."""

    changefreq = "monthly"

    PAGES = {"home": 1.0, "privacy": 0.3, "terms": 0.3}

    def items(self):
        return list(self.PAGES)

    def location(self, item):
        from django.urls import reverse
        return reverse(item)

    def priority(self, item):
        return self.PAGES[item]


def preview_404(request):
    """Debug-only helper so you can see the custom 404 page locally."""
    return page_not_found(request, Http404("preview"))


urlpatterns = [
    path("", views.home, name="home"),
    path("thank-you/", views.thanks, name="thanks"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
    # Browsers ask for these at the site root. On Vercel the CDN serves /static/ but WhiteNoise's root
    # files are not active, so forward them to the copies under /static/root/.
    path("favicon.ico", RedirectView.as_view(url="/static/root/favicon.ico", permanent=False)),
    path("apple-touch-icon.png", RedirectView.as_view(url="/static/root/apple-touch-icon.png", permanent=False)),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),
    path("sitemap.xml", sitemap, {"sitemaps": {"pages": PortfolioSitemap}}, name="sitemap"),
]
