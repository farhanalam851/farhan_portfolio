from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("core", "0002_content_models")]

    operations = [
        migrations.CreateModel(
            name="SiteProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(default="Farhan Alam", max_length=80)),
                ("email", models.EmailField(default="farhanalam8510@gmail.com", max_length=254)),
                ("location", models.CharField(default="Kanpur, Uttar Pradesh, India", max_length=120)),
                ("github", models.URLField(default="https://github.com/farhanalam851")),
                ("linkedin", models.URLField(default="https://www.linkedin.com/in/farhan-alam-b590b8408")),
                ("instagram", models.URLField(default="https://www.instagram.com/webby_farhan")),
                ("instagram_handle", models.CharField(default="@webby_farhan", max_length=60)),
                ("roles", models.TextField(
                    default="Django developer\nPython full-stack builder\nREST API engineer\nBCA student, shipping real projects",
                    help_text="Lines that type out in the hero. One per line.")),
                ("focus", models.TextField(
                    default="Full-stack web development\nDjango & DRF\nJavaScript\nREST APIs\nDatabase design\nProduction-ready client projects",
                    help_text="Ticked list in the About section. One per line.")),
                ("stat_projects", models.PositiveIntegerField(default=4, verbose_name="Hero number: projects")),
                ("stat_tech", models.PositiveIntegerField(default=9, verbose_name="Hero number: technologies")),
                ("reply_hours", models.PositiveIntegerField(default=24, verbose_name="Hero number: reply time (hours)")),
            ],
            options={"verbose_name": "site profile", "verbose_name_plural": "site profile"},
        ),
        migrations.CreateModel(
            name="TechLogo",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")),
                ("is_visible", models.BooleanField(default=True, help_text="Untick to hide from the site.")),
                ("row", models.PositiveSmallIntegerField(
                    choices=[(1, "Top strip (moves left)"), (2, "Bottom strip (moves right)")], default=1)),
                ("name", models.CharField(max_length=60)),
                ("icon", models.CharField(help_text="Devicon path, e.g. html5/html5-original.svg (see devicon.dev).", max_length=120)),
                ("invert", models.BooleanField(default=False, help_text="Tick for dark logos (Django, GitHub).")),
            ],
            options={"ordering": ["row", "order", "id"], "verbose_name": "moving logo"},
        ),
        migrations.CreateModel(
            name="ProcessStep",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")),
                ("is_visible", models.BooleanField(default=True, help_text="Untick to hide from the site.")),
                ("title", models.CharField(max_length=60)),
                ("text", models.CharField(max_length=200)),
            ],
            options={"ordering": ["order", "id"], "verbose_name": "process step"},
        ),
    ]
