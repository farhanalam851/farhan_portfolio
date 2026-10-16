from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("core", "0003_profile_logos_process")]

    operations = [
        migrations.AddField(
            model_name="project", name="live_url",
            field=models.URLField("Live site URL", blank=True,
                                  help_text="Deployed website. Adds a \"Live demo\" button and an automatic preview image."),
        ),
        migrations.AddField(
            model_name="project", name="image",
            field=models.CharField("Preview image", max_length=300, blank=True,
                                   help_text="Optional. A full https:// image URL, or a path under static/ (e.g. img/projects/mysite.jpg). Leave empty to auto-preview the live site."),
        ),
        migrations.AlterField(
            model_name="project", name="link",
            field=models.URLField(blank=True, help_text="GitHub repository URL."),
        ),
        migrations.AlterField(
            model_name="siteprofile", name="stat_projects",
            field=models.PositiveIntegerField(default=4, verbose_name="Hero number: projects"),
        ),
    ]
