from django.db import migrations

REMOVED = ["B2B Clothing E-Commerce Platform", "Django Blog Platform"]


def remove(apps, schema_editor):
    apps.get_model("core", "Project").objects.filter(title__in=REMOVED).delete()


class Migration(migrations.Migration):

    dependencies = [("core", "0004_project_live_url_image")]

    operations = [migrations.RunPython(remove, migrations.RunPython.noop)]
