"""Run with:  python manage.py test   (leave DEBUG unset so static files resolve without collectstatic)."""
import re

from django.test import TestCase, override_settings

from .models import ContactMessage

VALID = {"name": "Asha Verma", "email": "asha@company.com", "topic": "job",
         "message": "Hi Farhan, we are hiring a junior Django developer."}


def title_of(html):
    return re.search(r"<title>(.*?)</title>", html).group(1)


class PageTests(TestCase):
    def test_public_pages_render_with_unique_titles_and_descriptions(self):
        titles = set()
        for url in ["/", "/privacy/", "/terms/", "/thank-you/"]:
            r = self.client.get(url)
            self.assertEqual(r.status_code, 200, url)
            html = r.content.decode()
            titles.add(title_of(html))
            self.assertRegex(html, r'<meta name="description" content="[^"]{40,}"', url)
            self.assertNotIn("{%", html)
        self.assertEqual(len(titles), 4)

    def test_home_meta_is_within_search_limits(self):
        html = self.client.get("/").content.decode()
        self.assertLessEqual(len(title_of(html)), 70)
        desc = re.search(r'name="description" content="(.*?)"', html).group(1)
        self.assertLessEqual(len(desc), 160)
        self.assertIn('rel="canonical"', html)
        self.assertIn("og:image", html)
        self.assertIn("application/ld+json", html)

    def test_every_image_has_alt_text(self):
        for url in ["/", "/privacy/", "/thank-you/"]:
            html = self.client.get(url).content.decode()
            for tag in re.findall(r"<img\b[^>]*>", html):
                self.assertRegex(tag, r'\balt="[^"]+"', tag)

    def test_above_the_fold_cta_and_mobile_cta_exist(self):
        html = self.client.get("/").content.decode()
        self.assertIn('data-track="cta_start_project"', html)
        self.assertIn('id="mobileCta"', html)
        self.assertIn('id="cookieBanner"', html)

    def test_thank_you_is_noindex_and_not_in_sitemap(self):
        self.assertIn("noindex", self.client.get("/thank-you/").content.decode())
        sitemap = self.client.get("/sitemap.xml").content.decode()
        self.assertEqual(re.findall(r"<loc>(.*?)</loc>", sitemap),
                         ["http://testserver/", "http://testserver/privacy/", "http://testserver/terms/"])

    def test_robots_txt(self):
        r = self.client.get("/robots.txt")
        self.assertTrue(r["Content-Type"].startswith("text/plain"))
        body = r.content.decode()
        self.assertIn("Disallow: /admin/", body)
        self.assertIn("Sitemap: http://testserver/sitemap.xml", body)

    def test_icons_served_from_site_root(self):
        self.assertEqual(self.client.get("/favicon.ico").status_code, 200)
        self.assertEqual(self.client.get("/apple-touch-icon.png").status_code, 200)

    def test_custom_404_page(self):
        r = self.client.get("/definitely-not-a-page/")
        self.assertEqual(r.status_code, 404)
        html = r.content.decode()
        self.assertIn("This page wandered off", html)
        self.assertIn("noindex", html)

    def test_500_template_is_standalone(self):
        from django.template.loader import render_to_string
        self.assertIn("Something broke", render_to_string("500.html"))


class ContactFormTests(TestCase):
    def test_invalid_submission_shows_errors_and_saves_nothing(self):
        r = self.client.post("/", {**VALID, "name": "A", "email": "nope", "message": "short"})
        html = r.content.decode()
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(html.count("is-invalid"), 3)
        self.assertIn('aria-invalid="true"', html)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_honeypot_blocks_bots(self):
        r = self.client.post("/", {**VALID, "contact_hp": "spam.example"})
        self.assertRedirects(r, "/thank-you/", fetch_redirect_response=False)  # bot is not told it failed
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_database_failure_shows_friendly_message_not_500(self):
        from unittest import mock
        with mock.patch("core.forms.ContactForm.save", side_effect=RuntimeError("db down")):
            r = self.client.post("/", VALID)
        self.assertEqual(r.status_code, 200)
        self.assertIn("could not be saved", r.content.decode())

    def test_csrf_failure_page_is_readable(self):
        from django.test import Client
        r = Client(enforce_csrf_checks=True).post("/", VALID)
        self.assertEqual(r.status_code, 403)
        self.assertIn("Please try again", r.content.decode())

    def test_valid_submission_redirects_to_thank_you_and_fires_event_once(self):
        r = self.client.post("/", VALID)
        self.assertRedirects(r, "/thank-you/", fetch_redirect_response=False)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertIn('data-page-event="generate_lead"', self.client.get("/thank-you/").content.decode())
        self.assertNotIn("data-page-event", self.client.get("/thank-you/").content.decode())

    def test_direct_visit_to_thank_you_does_not_count_as_enquiry(self):
        self.assertNotIn("data-page-event", self.client.get("/thank-you/").content.decode())


class AnalyticsTests(TestCase):
    def test_analytics_off_by_default(self):
        self.assertNotIn("window.GA_ID", self.client.get("/").content.decode())

    @override_settings(GA_MEASUREMENT_ID="G-ABC123XYZ")
    def test_measurement_id_is_exposed_when_configured(self):
        self.assertIn("window.GA_ID", self.client.get("/").content.decode())


class ProjectShowcaseTests(TestCase):
    def test_new_client_projects_show_live_and_github_links(self):
        html = self.client.get("/").content.decode()
        for live, repo in [("https://ffmanufacturer.vercel.app/", "https://github.com/farhanalam851/ffmanufacturer"),
                           ("https://lalasarees-site.vercel.app/", "https://github.com/farhanalam851/lalasarees_site")]:
            self.assertIn(f'href="{live}"', html)
            self.assertIn(f'href="{repo}"', html)
            self.assertIn(f"image.thum.io/get/width/1200/crop/750/{live}", html)

    def test_removed_projects_are_gone(self):
        html = self.client.get("/").content.decode()
        self.assertNotIn("Django Blog Platform", html)
        self.assertNotIn("B2B Clothing E-Commerce Platform", html)

    def test_seed_adds_missing_projects_to_an_existing_database(self):
        from django.core.management import call_command
        from .models import Project
        call_command("seed_content")
        Project.objects.filter(title__startswith="F.F").delete()
        call_command("seed_content")
        titles = list(Project.objects.values_list("title", flat=True))
        self.assertEqual(len(titles), len(set(titles)))
        self.assertEqual(Project.objects.count(), 4)
