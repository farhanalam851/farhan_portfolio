from django.core.management.base import BaseCommand

from core import data
from core.models import JourneyItem, ProcessStep, Project, Service, SiteProfile, Skill, TechLogo


class Command(BaseCommand):
    help = "Copy the starter content from core/data.py into the database so it can be edited in /admin/."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Delete existing content and re-seed.")

    def handle(self, *args, **opts):
        if opts["force"]:
            for m in (Project, Skill, Service, JourneyItem, TechLogo, ProcessStep, SiteProfile):
                m.objects.all().delete()

        if not SiteProfile.objects.exists():
            p = data.PROFILE
            SiteProfile.objects.create(
                name=p["name"], email=p["email"], location=p["location"], github=p["github"],
                linkedin=p["linkedin"], instagram=p["instagram"], instagram_handle=p["instagram_handle"],
                roles="\n".join(p["roles"]), focus="\n".join(data.FOCUS),
                stat_projects=p["stat_projects"], stat_tech=p["stat_tech"], reply_hours=p["reply_hours"],
            )
        if not TechLogo.objects.exists():
            for row, logos in ((1, data.LOGOS_ROW_1), (2, data.LOGOS_ROW_2)):
                for i, l in enumerate(logos):
                    TechLogo.objects.create(row=row, order=i * 10, name=l["name"], icon=l["icon"],
                                            invert=l.get("invert", False))
        if not ProcessStep.objects.exists():
            for i, (_n, title, text) in enumerate(data.PROCESS):
                ProcessStep.objects.create(order=i * 10, title=title, text=text)

        # Adds any project from data.py that is not in the database yet, so existing sites pick up new ones.
        existing = Project.objects.exists()
        added = 0
        for i, p in enumerate(data.PROJECTS):
            if Project.objects.filter(title=p["title"]).exists():
                continue
            Project.objects.create(
                order=(1 + added) if existing else i * 10, title=p["title"], kind=p["kind"], summary=p["summary"],
                points="\n".join(p["points"]), stack=", ".join(p["stack"]),
                link=p["link"], live_url=p.get("live_url", ""), image=p.get("image", ""),
                featured=p.get("featured", False),
            )
            added += 1

        if not Skill.objects.exists():
            for i, s in enumerate(data.SKILLS):
                Skill.objects.create(
                    order=i * 10, name=s["name"], icon=s["icon"], invert=s.get("invert", False),
                    tag=s["tag"], text=s["text"],
                )
        if not Service.objects.exists():
            for i, s in enumerate(data.SERVICES):
                Service.objects.create(order=i * 10, icon=s["icon"], title=s["title"], text=s["text"])
        if not JourneyItem.objects.exists():
            for i, j in enumerate(data.JOURNEY):
                JourneyItem.objects.create(order=i * 10, when=j["when"], title=j["title"], text=j["text"])

        self.stdout.write(self.style.SUCCESS(
            f"Content ready: {Project.objects.count()} projects, {Skill.objects.count()} skills, "
            f"{Service.objects.count()} services, {JourneyItem.objects.count()} journey items."
        ))
