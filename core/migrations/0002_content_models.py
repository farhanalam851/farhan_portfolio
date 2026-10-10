from django.db import migrations, models


def _order_fields():
    return [
        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
        ("order", models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")),
        ("is_visible", models.BooleanField(default=True, help_text="Untick to hide from the site.")),
    ]


class Migration(migrations.Migration):

    dependencies = [("core", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=_order_fields() + [
                ("title", models.CharField(max_length=120)),
                ("kind", models.CharField(help_text="e.g. Full-stack - Django", max_length=60)),
                ("summary", models.TextField()),
                ("points", models.TextField(blank=True, help_text="One bullet point per line.")),
                ("stack", models.CharField(blank=True, help_text="Comma separated, e.g. Django, Bootstrap, SQL", max_length=200)),
                ("link", models.URLField(blank=True, help_text="GitHub or live site URL.")),
                ("featured", models.BooleanField(default=False, help_text="Shows as the big wide card.")),
            ],
            options={"ordering": ["order", "id"], "abstract": False},
        ),
        migrations.CreateModel(
            name="Skill",
            fields=_order_fields() + [
                ("name", models.CharField(max_length=80)),
                ("icon", models.CharField(help_text="Devicon path, e.g. python/python-original.svg (see devicon.dev).", max_length=120)),
                ("invert", models.BooleanField(default=False, help_text="Tick for dark logos (Django, GitHub) so they show in dark mode.")),
                ("tag", models.CharField(help_text="Short label, e.g. Main framework", max_length=80)),
                ("text", models.CharField(max_length=220)),
            ],
            options={"ordering": ["order", "id"], "abstract": False},
        ),
        migrations.CreateModel(
            name="Service",
            fields=_order_fields() + [
                ("icon", models.CharField(default="bi-briefcase", help_text="Bootstrap Icons class, e.g. bi-briefcase (see icons.getbootstrap.com).", max_length=60)),
                ("title", models.CharField(max_length=80)),
                ("text", models.CharField(max_length=240)),
            ],
            options={"ordering": ["order", "id"], "abstract": False},
        ),
        migrations.CreateModel(
            name="JourneyItem",
            fields=_order_fields() + [
                ("when", models.CharField(help_text="e.g. Now, 2025, Before", max_length=40)),
                ("title", models.CharField(max_length=140)),
                ("text", models.TextField()),
            ],
            options={"ordering": ["order", "id"], "verbose_name": "journey item"},
        ),
    ]
