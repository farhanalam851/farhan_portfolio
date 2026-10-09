from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "topic", "created_at", "is_read")
    list_filter = ("topic", "is_read", "created_at")
    search_fields = ("name", "email", "message")
    list_editable = ("is_read",)
    readonly_fields = ("created_at",)
