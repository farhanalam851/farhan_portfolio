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
