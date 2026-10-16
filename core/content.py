"""Shared helpers that load site content from the admin panel (falling back to core/data.py)."""
from . import data
from .models import JourneyItem, ProcessStep, Project, Service, SiteProfile, Skill, TechLogo


def lines(text):
    return [ln.strip() for ln in (text or "").splitlines() if ln.strip()]


def csv(text):
    return [t.strip() for t in (text or "").split(",") if t.strip()]


def preview_image(live_url, image=""):
    """Explicit image wins; otherwise a live screenshot of the deployed site."""
    if image:
        return image
    if live_url:
        return f"https://image.thum.io/get/width/1200/crop/750/{live_url}"
    return ""


def get_profile(request=None):
    """Profile from the admin panel; falls back to core/data.py. Cached per request."""
    if request is not None and hasattr(request, "_site_profile"):
        return request._site_profile

    p = dict(data.PROFILE)
    p["focus"] = list(data.FOCUS)
    obj = SiteProfile.objects.first()
    if obj:
        p.update({
            "name": obj.name, "email": obj.email, "location": obj.location,
            "github": obj.github, "linkedin": obj.linkedin, "instagram": obj.instagram,
            "instagram_handle": obj.instagram_handle,
            "stat_projects": obj.stat_projects, "stat_tech": obj.stat_tech,
            "reply_hours": obj.reply_hours,
        })
        roles = lines(obj.roles)
        if roles:
            p["roles"] = roles
        focus = lines(obj.focus)
        if focus:
            p["focus"] = focus

    if request is not None:
        request._site_profile = p
    return p


def get_content():
    projects = [
        {"title": p.title, "kind": p.kind, "summary": p.summary, "points": lines(p.points),
         "stack": csv(p.stack), "link": p.link or "#", "featured": p.featured,
         "live_url": p.live_url, "image": preview_image(p.live_url, p.image)}
        for p in Project.objects.filter(is_visible=True)
    ]
    skills = [
        {"name": s.name, "icon": s.icon, "invert": s.invert, "tag": s.tag, "text": s.text}
        for s in Skill.objects.filter(is_visible=True)
    ]
    services = [
        {"icon": s.icon, "title": s.title, "text": s.text}
        for s in Service.objects.filter(is_visible=True)
    ]
    journey = [
        {"when": j.when, "title": j.title, "text": j.text}
        for j in JourneyItem.objects.filter(is_visible=True)
    ]
    logos = list(TechLogo.objects.filter(is_visible=True))
    logos_1 = [{"name": l.name, "icon": l.icon, "invert": l.invert} for l in logos if l.row == 1]
    logos_2 = [{"name": l.name, "icon": l.icon, "invert": l.invert} for l in logos if l.row == 2]
    steps = [
        (f"{i:02d}", s.title, s.text)
        for i, s in enumerate(ProcessStep.objects.filter(is_visible=True), start=1)
    ]
    return {
        "logos_1": logos_1 or data.LOGOS_ROW_1,
        "logos_2": logos_2 or data.LOGOS_ROW_2,
        "process": steps or data.PROCESS,
        "projects": projects or [dict(p, image=preview_image(p.get("live_url", ""), p.get("image", ""))) for p in data.PROJECTS],
        "skills": skills or data.SKILLS,
        "services": services or data.SERVICES,
        "journey": journey or data.JOURNEY,
    }
