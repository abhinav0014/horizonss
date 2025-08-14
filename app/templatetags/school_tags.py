from django import template
from app.models import Notice, Event, Faculty

register = template.Library()

@register.simple_tag
def get_latest_notices(count=3):
    return Notice.objects.filter(notice_type='IMPORTANT').order_by('-created_at')[:count]

@register.simple_tag
def get_upcoming_events(count=3):
    return Event.objects.filter(is_completed=False).order_by('start_date')[:count]

@register.simple_tag
def get_school_stats():
    return {
        'students': 1500,
        'teachers': 120,
        'success_rate': 98,
        'programs': 50
    }

@register.simple_tag
def get_faculty_members():
    return Faculty.objects.filter(is_active=True)[:8]