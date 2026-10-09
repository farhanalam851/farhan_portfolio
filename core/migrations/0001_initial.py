from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ContactMessage",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("email", models.EmailField(max_length=254)),
                (
                    "topic",
                    models.CharField(
                        choices=[
                            ("website", "Business website"),
                            ("ecommerce", "E-commerce store"),
                            ("webapp", "Custom web application"),
                            ("api", "REST API / backend"),
                            ("job", "Job / internship opportunity"),
                            ("other", "Something else"),
                        ],
                        default="website",
                        max_length=20,
                    ),
                ),
                ("message", models.TextField(max_length=3000)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_read", models.BooleanField(default=False)),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
