from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
import calendar
from datetime import datetime, timedelta
import csv
from .models import Notice, Event, Subscriber

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def overview(request):
    # Calculate counts for stats
    total_notices = Notice.objects.count()
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(
        date__gte=timezone.now()
    ).count()


    context = {
        'active_tab': 'overview',
        'notices': Notice.objects.all()[:5],  # Get last 5 notices
        'events': Event.objects.all()[:5],  # Get last 5 events
        'subscribers': Subscriber.objects.all()[:5],
        'stats': {
            'total_notices': total_notices,
            'total_events': total_events,
            'upcoming_events': upcoming_events,
        }
    }
    return render(request, 'dash-overview.html', context)

@user_passes_test(is_admin)
def notice_list(request):
    context = {
        'active_tab': 'notices',
        'notices': Notice.objects.all().order_by('-created_at'),
        'notice_types': Notice.NOTICE_TYPES,  # For the add/edit form
        'stats': {
            'total': Notice.objects.count(),
            'general': Notice.objects.filter(notice_type='GENERAL').count(),
            'events': Notice.objects.filter(notice_type='EVENT').count(),
            'important': Notice.objects.filter(notice_type='IMPORTANT').count(),
        }
    }
    return render(request, 'dash-notice_list.html', context)

@user_passes_test(is_admin)
def events(request):
    today = timezone.now()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    
    # Get calendar info
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    
    # Get events for the current month
    events_in_month = Event.objects.filter(
        date__year=year,
        date__month=month
    ).order_by('date', 'time')
    
    # Create a dict of dates with events
    event_dates = {}
    for event in events_in_month:
        event_dates[event.date.day] = {
            'count': event_dates.get(event.date.day, {}).get('count', 0) + 1,
            'events': event_dates.get(event.date.day, {}).get('events', []) + [event]
        }
    
    # Get navigation dates
    prev_month = datetime(year, month, 1) - timedelta(days=1)
    next_month = datetime(year, month % 12 + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
    
    context = {
        'active_tab': 'events',
        'calendar': cal,
        'month_name': month_name,
        'year': year,
        'event_dates': event_dates,
        'prev_month': {'year': prev_month.year, 'month': prev_month.month},
        'next_month': {'year': next_month.year, 'month': next_month.month},
        'upcoming_events': Event.objects.filter(
            date__gte=today.date()
        ).order_by('date', 'time')[:5],
        'stats': {
            'total_events': Event.objects.count(),
            'upcoming_events': Event.objects.filter(date__gte=today.date()).count(),
            'this_month': events_in_month.count(),
        }
    }
    return render(request, 'dash-events.html', context)

@user_passes_test(is_admin)
def subscribers(request):
    # Note: You'll need to create a Subscriber model and import it
    # For now, using placeholder data
    context = {
        'active_tab': 'subscribers',
        'subscribers': Subscriber.objects.all(),
        'active_subscribers': Subscriber.objects.filter(is_active=True).count(),
        'new_subscribers': Subscriber.objects.filter(created_at__month=timezone.now().month).count(),
        'stats': {
            'total': Subscriber.objects.count(),
            'active': Subscriber.objects.filter(is_active=True).count(),
            'this_month': Subscriber.objects.filter(created_at__month=timezone.now().month).count(),
        }
    }
    return render(request, 'dash-subscribers.html', context)

@user_passes_test(is_admin)
def export_subscribers(request):
    # Create the HttpResponse object with CSV header
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="subscribers.csv"'},
    )
    
    # Create CSV writer
    writer = csv.writer(response)
    writer.writerow(['Email', 'Name', 'Status', 'Joined Date'])
    
    # Get all subscribers and write to CSV
    subscribers = Subscriber.objects.all()
    for subscriber in subscribers:
        writer.writerow([
            subscriber.email,
            subscriber.name,
            'Active' if subscriber.is_active else 'Inactive',
            subscriber.created_at.strftime('%Y-%m-%d')
        ])
    
    return response

@user_passes_test(is_admin)
def delete_subscriber(request, subscriber_id):
    if request.method == 'POST':
        subscriber = get_object_or_404(Subscriber, id=subscriber_id)
        subscriber.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)