from django.contrib import admin

from .models import (ContactMessage, JourneyItem, ProcessStep, Project, Service,
                     SiteProfile, Skill, TechLogo)

admin.site.site_header = "Farhan's Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Manage your portfolio"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "topic", "created_at", "is_read")
    list_filter = ("topic", "is_read", "created_at")
    search_fields = ("name", "email", "message")
    list_editable = ("is_read",)
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"


class OrderedAdmin(admin.ModelAdmin):
    list_editable = ("order", "is_visible")
    ordering = ("order", "id")


@admin.register(Project)
class ProjectAdmin(OrderedAdmin):
    list_display = ("title", "kind", "featured", "order", "is_visible")
    search_fields = ("title", "summary")


@admin.register(Skill)
class SkillAdmin(OrderedAdmin):
    list_display = ("name", "tag", "order", "is_visible")


@admin.register(Service)
class ServiceAdmin(OrderedAdmin):
    list_display = ("title", "icon", "order", "is_visible")


@admin.register(JourneyItem)
class JourneyItemAdmin(OrderedAdmin):
    list_display = ("title", "when", "order", "is_visible")


@admin.register(TechLogo)
class TechLogoAdmin(OrderedAdmin):
    list_display = ("name", "row", "order", "is_visible")
    list_filter = ("row",)
    ordering = ("row", "order", "id")


@admin.register(ProcessStep)
class ProcessStepAdmin(OrderedAdmin):
    list_display = ("title", "order", "is_visible")


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    """Only one profile record: edit it, never add a second or delete it."""

    fieldsets = (
        ("Identity", {"fields": ("name", "location", "email")}),
        ("Links", {"fields": ("github", "linkedin", "instagram", "instagram_handle")}),
        ("Hero & About text", {"fields": ("roles", "focus")}),
        ("Hero numbers", {"fields": ("stat_projects", "stat_tech", "reply_hours")}),
    )

    def has_add_permission(self, request):
        return not SiteProfile.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
