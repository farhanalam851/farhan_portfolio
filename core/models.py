from django.db import models


class ContactMessage(models.Model):
    SERVICE_CHOICES = [
        ("website", "Business website"),
        ("ecommerce", "E-commerce store"),
        ("webapp", "Custom web application"),
        ("api", "REST API / backend"),
        ("job", "Job / internship opportunity"),
        ("other", "Something else"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    topic = models.CharField(max_length=20, choices=SERVICE_CHOICES, default="website")
    message = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.get_topic_display()}"


class OrderedContent(models.Model):
    """Shared fields for everything shown on the site."""

    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")
    is_visible = models.BooleanField(default=True, help_text="Untick to hide from the site.")

    class Meta:
        abstract = True
        ordering = ["order", "id"]


class Project(OrderedContent):
    title = models.CharField(max_length=120)
    kind = models.CharField(max_length=60, help_text="e.g. Full-stack - Django")
    summary = models.TextField()
    points = models.TextField(blank=True, help_text="One bullet point per line.")
    stack = models.CharField(max_length=200, blank=True, help_text="Comma separated, e.g. Django, Bootstrap, SQL")
    link = models.URLField(blank=True, help_text="GitHub repository URL.")
    live_url = models.URLField("Live site URL", blank=True, help_text="Deployed website. Adds a \"Live demo\" button and an automatic preview image.")
    image = models.CharField("Preview image", max_length=300, blank=True,
                             help_text="Optional. A full https:// image URL, or a path under static/ (e.g. img/projects/mysite.jpg). Leave empty to auto-preview the live site.")
    featured = models.BooleanField(default=False, help_text="Shows as the big wide card.")

    class Meta(OrderedContent.Meta):
        pass

    def __str__(self):
        return self.title


class Skill(OrderedContent):
    name = models.CharField(max_length=80)
    icon = models.CharField(
        max_length=120,
        help_text="Devicon path, e.g. python/python-original.svg (see devicon.dev).",
    )
    invert = models.BooleanField(default=False, help_text="Tick for dark logos (Django, GitHub) so they show in dark mode.")
    tag = models.CharField(max_length=80, help_text="Short label, e.g. Main framework")
    text = models.CharField(max_length=220)

    class Meta(OrderedContent.Meta):
        pass

    def __str__(self):
        return self.name


class Service(OrderedContent):
    icon = models.CharField(max_length=60, default="bi-briefcase", help_text="Bootstrap Icons class, e.g. bi-briefcase (see icons.getbootstrap.com).")
    title = models.CharField(max_length=80)
    text = models.CharField(max_length=240)

    class Meta(OrderedContent.Meta):
        pass

    def __str__(self):
        return self.title


class JourneyItem(OrderedContent):
    when = models.CharField(max_length=40, help_text="e.g. Now, 2025, Before")
    title = models.CharField(max_length=140)
    text = models.TextField()

    class Meta(OrderedContent.Meta):
        verbose_name = "journey item"

    def __str__(self):
        return self.title


class SiteProfile(models.Model):
    """Single record with your name, links and hero details."""

    name = models.CharField(max_length=80, default="Farhan Alam")
    email = models.EmailField(default="farhanalam8510@gmail.com")
    location = models.CharField(max_length=120, default="Kanpur, Uttar Pradesh, India")
    github = models.URLField(default="https://github.com/farhanalam851")
    linkedin = models.URLField(default="https://www.linkedin.com/in/farhan-alam-b590b8408")
    instagram = models.URLField(default="https://www.instagram.com/webby_farhan")
    instagram_handle = models.CharField(max_length=60, default="@webby_farhan")
    roles = models.TextField(
        default="Django developer\nPython full-stack builder\nREST API engineer\nBCA student, shipping real projects",
        help_text="Lines that type out in the hero. One per line.",
    )
    focus = models.TextField(
        default="Full-stack web development\nDjango & DRF\nJavaScript\nREST APIs\nDatabase design\nProduction-ready client projects",
        help_text="Ticked list in the About section. One per line.",
    )
    stat_projects = models.PositiveIntegerField("Hero number: projects", default=4)
    stat_tech = models.PositiveIntegerField("Hero number: technologies", default=9)
    reply_hours = models.PositiveIntegerField("Hero number: reply time (hours)", default=24)

    class Meta:
        verbose_name = "site profile"
        verbose_name_plural = "site profile"

    def __str__(self):
        return self.name


class TechLogo(OrderedContent):
    ROW_CHOICES = [(1, "Top strip (moves left)"), (2, "Bottom strip (moves right)")]

    row = models.PositiveSmallIntegerField(choices=ROW_CHOICES, default=1)
    name = models.CharField(max_length=60)
    icon = models.CharField(max_length=120, help_text="Devicon path, e.g. html5/html5-original.svg (see devicon.dev).")
    invert = models.BooleanField(default=False, help_text="Tick for dark logos (Django, GitHub).")

    class Meta:
        ordering = ["row", "order", "id"]
        verbose_name = "moving logo"

    def __str__(self):
        return self.name


class ProcessStep(OrderedContent):
    title = models.CharField(max_length=60)
    text = models.CharField(max_length=200)

    class Meta(OrderedContent.Meta):
        verbose_name = "process step"

    def __str__(self):
        return self.title
