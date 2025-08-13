from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
import calendar
from datetime import datetime, timedelta
import csv
import json
from .models import Notice, Event, Subscriber, Admission
from .forms import EventForm, NoticeForm

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


    # Add admission stats
    admission_stats = {
        'total': Admission.objects.count(),
        'pending': Admission.objects.filter(status='PENDING').count(),
        'accepted': Admission.objects.filter(status='ACCEPTED').count(),
        'rejected': Admission.objects.filter(status='REJECTED').count(),
    }
    
    context = {
        'active_tab': 'overview',
        'notices': Notice.objects.all()[:5],  # Get last 5 notices
        'events': Event.objects.all()[:5],  # Get last 5 events
        'subscribers': Subscriber.objects.all()[:5],
        'stats': {
            'total_notices': total_notices,
            'total_events': total_events,
            'upcoming_events': upcoming_events,
        },
        'admission_stats': admission_stats,
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
def create_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.author = request.user
            notice.save()
            return JsonResponse({
                'status': 'success',
                'notice': {
                    'id': notice.id,
                    'title': notice.title,
                    'type': notice.get_notice_type_display(),
                    'date': notice.created_at.strftime('%Y-%m-%d'),
                    'image_url': notice.image.url if notice.image else None
                }
            })
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    return JsonResponse({'status': 'error'}, status=405)

@user_passes_test(is_admin)
def edit_notice(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES, instance=notice)
        if form.is_valid():
            notice = form.save()
            return JsonResponse({
                'status': 'success',
                'notice': {
                    'id': notice.id,
                    'title': notice.title,
                    'type': notice.get_notice_type_display(),
                    'date': notice.created_at.strftime('%Y-%m-%d'),
                    'image_url': notice.image.url if notice.image else None
                }
            })
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    return JsonResponse({
        'notice': {
            'id': notice.id,
            'title': notice.title,
            'content': notice.content,
            'notice_type': notice.notice_type,
            'image_url': notice.image.url if notice.image else None
        }
    })

@user_passes_test(is_admin)
def delete_notice(request, notice_id):
    if request.method == 'POST':
        notice = get_object_or_404(Notice, id=notice_id)
        notice.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@user_passes_test(is_admin)
def events(request):
    today = timezone.now()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    view = request.GET.get('view', 'upcoming')  # Add view parameter
    
    # Get calendar info
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    
    # Get events based on view
    events_query = Event.objects.filter(date__year=year, date__month=month)
    if view == 'completed':
        events_in_month = events_query.filter(is_completed=True)
        upcoming_events = Event.objects.filter(is_completed=True).order_by('-completed_at')[:5]
    else:
        events_in_month = events_query.filter(is_completed=False)
        upcoming_events = Event.objects.filter(
            date__gte=today.date(),
            is_completed=False
        ).order_by('date', 'time')[:5]
    
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
        'view': view,
        'event_dates': event_dates,
        'prev_month': {'year': prev_month.year, 'month': prev_month.month},
        'next_month': {'year': next_month.year, 'month': next_month.month},
        'upcoming_events': upcoming_events,
        'stats': {
            'total_events': Event.objects.count(),
            'upcoming_events': Event.objects.filter(date__gte=today.date(), is_completed=False).count(),
            'completed_events': Event.objects.filter(is_completed=True).count(),
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

@user_passes_test(is_admin)
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            return JsonResponse({
                'status': 'success',
                'event': {
                    'id': event.id,
                    'title': event.title,
                    'date': event.date.strftime('%Y-%m-%d'),
                    'time': event.time.strftime('%H:%M'),
                    'venue': event.venue
                }
            })
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    return JsonResponse({'status': 'error'}, status=405)

@user_passes_test(is_admin)
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            return JsonResponse({
                'status': 'success',
                'event': {
                    'id': event.id,
                    'title': event.title,
                    'date': event.date.strftime('%Y-%m-%d'),
                    'time': event.time.strftime('%H:%M'),
                    'venue': event.venue
                }
            })
        return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)
    
    # Return event data for GET request
    return JsonResponse({
        'event': {
            'id': event.id,
            'title': event.title,
            'description': event.description,
            'event_type': event.event_type,
            'date': event.date.strftime('%Y-%m-%d'),
            'time': event.time.strftime('%H:%M'),
            'venue': event.venue,
            'is_active': event.is_active
        }
    })

@user_passes_test(is_admin)
def delete_event(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        event.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@user_passes_test(is_admin)
def toggle_event_completion(request, event_id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=event_id)
        event.is_completed = not event.is_completed
        event.completed_at = timezone.now() if event.is_completed else None
        event.save()
        return JsonResponse({
            'status': 'success',
            'is_completed': event.is_completed,
            'completed_at': event.completed_at.strftime('%Y-%m-%d %H:%M') if event.completed_at else None
        })
    return JsonResponse({'status': 'error'}, status=400)

@user_passes_test(is_admin)
def admissions(request):
    status_filter = request.GET.get('status', 'all')
    
    # Base queryset
    admissions = Admission.objects.all()
    
    # Apply filters
    if status_filter != 'all':
        admissions = admissions.filter(status=status_filter.upper())
    
    # Get stats
    stats = {
        'total': Admission.objects.count(),
        'pending': Admission.objects.filter(status='PENDING').count(),
        'accepted': Admission.objects.filter(status='ACCEPTED').count(),
        'rejected': Admission.objects.filter(status='REJECTED').count(),
    }
    
    context = {
        'active_tab': 'admissions',
        'admissions': admissions,
        'stats': stats,
        'current_filter': status_filter
    }
    return render(request, 'dash-admissions.html', context)

@user_passes_test(is_admin)
def admission_detail(request, admission_id):
    admission = get_object_or_404(Admission, id=admission_id)
    return JsonResponse({
        'id': admission.id,
        'application_id': admission.application_id,
        'full_name': admission.full_name,
        'date_of_birth': admission.date_of_birth.strftime('%Y-%m-%d'),
        'gender': admission.get_gender_display(),
        'email': admission.email,
        'phone': admission.phone,
        'address': admission.address,
        'applying_for_grade': admission.applying_for_grade,
        'previous_school': admission.previous_school,
        'previous_grade': admission.previous_grade,
        'previous_percentage': str(admission.previous_percentage),
        'father_name': admission.father_name,
        'father_occupation': admission.father_occupation,
        'father_phone': admission.father_phone,
        'mother_name': admission.mother_name,
        'mother_occupation': admission.mother_occupation,
        'mother_phone': admission.mother_phone,
        'status': admission.get_status_display(),
        'applied_at': admission.applied_at.strftime('%B %d, %Y'),
        'student_photo': admission.student_photo.url if admission.student_photo else None,
        'documents': {
            'marksheet': admission.previous_marksheet.url if admission.previous_marksheet else None,
            'transfer_certificate': admission.transfer_certificate.url if admission.transfer_certificate else None,
        }
    })

@user_passes_test(is_admin)
def update_admission_status(request, admission_id):
    if request.method == 'POST':
        try:
            admission = get_object_or_404(Admission, id=admission_id)
            data = json.loads(request.body)
            status = data.get('status')
            
            if status in ['ACCEPTED', 'REJECTED']:
                admission.status = status
                admission.save()
                return JsonResponse({'status': 'success'})
            
            return JsonResponse({'status': 'error', 'message': 'Invalid status'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)