from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Notice, Event, Admission
from calendar import monthcalendar
from datetime import datetime
from django.http import JsonResponse
from .models import Subscriber
import json

def home(request):
    context = {
        'latest_notices': Notice.objects.all()[:5],
        'upcoming_events': Event.objects.filter(is_completed=False)[:3],
        'total_students': 1500,  # You can make these dynamic from your database
        'success_rate': 98,
        'featured_programs': [
            {
                'name': 'Science Stream',
                'description': 'Comprehensive science education with modern lab facilities',
                'icon': 'flask'
            },
            {
                'name': 'Management Stream',
                'description': 'Business and management studies with practical exposure',
                'icon': 'chart-line'
            },
            {
                'name': 'Humanities',
                'description': 'Liberal arts and humanities with critical thinking focus',
                'icon': 'book-open'
            }
        ]
    }
    return render(request, 'index.html', context)


def about(request):
    context = {
        'school_history': {
            'founded': 1990,
            'founder': "Founder's Name",
            'achievements': [
                'National Award for Excellence in Education 2020',
                'Best School in the Region 2021',
                'Outstanding Academic Performance 2022'
            ]
        }
    }
    return render(request, 'about.html', context)

def notices(request):
    notices = Notice.objects.all().order_by('-created_at')
    context = {
        'notices': notices
    }
    return render(request, 'notices.html', context)


def events(request):
    today = datetime.now()
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    
    # Get calendar data
    calendar_data = monthcalendar(year, month)
    month_name = today.replace(day=1, month=month, year=year).strftime('%B')
    
    # Get events for the month
    events = Event.objects.filter(
        start_date__year=year,
        start_date__month=month
    ).order_by('start_date', 'start_time')
    
    # Organize events by date
    event_dates = {}
    for event in events:
        day = event.start_date.day
        if day not in event_dates:
            event_dates[day] = {
                'events': [],
                'count': 0,
                'is_completed': True
            }
        event_dates[day]['events'].append(event)
        event_dates[day]['count'] += 1
        if not event.is_completed:
            event_dates[day]['is_completed'] = False
    
    # Calculate next and previous months
    if month == 12:
        next_month = {'year': year + 1, 'month': 1}
    else:
        next_month = {'year': year, 'month': month + 1}
        
    if month == 1:
        prev_month = {'year': year - 1, 'month': 12}
    else:
        prev_month = {'year': year, 'month': month - 1}
    
    context = {
        'calendar': calendar_data,
        'day_names': ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
        'month_name': month_name,
        'year': year,
        'month': month,
        'next_month': next_month,
        'prev_month': prev_month,
        'today_day': today.day,
        'today_month': today.month,
        'today_year': today.year,
        'event_dates': event_dates
    }
    return render(request, 'events.html', context)

def contact(request):
    if request.method == 'POST':
        # Handle contact form submission
        # Add your email sending logic here
        return JsonResponse({'status': 'success'})
    return render(request, 'contact.html')

def create_or_update_event(request, event_id=None):
    if request.method == 'POST':
        try:
            data = request.POST.dict()
            if event_id:
                event = Event.objects.get(id=event_id)
            else:
                event = Event()

            event.title = data.get('title')
            event.description = data.get('description')
            event.event_type = data.get('event_type')
            event.venue = data.get('venue')
            event.is_active = data.get('is_active') == 'on'
            
            # Handle dates and times
            event.start_date = data.get('start_date')
            event.start_time = data.get('start_time')
            
            # Handle range events
            if data.get('is_range') == 'on':
                event.end_date = data.get('end_date')
                event.end_time = data.get('end_time')
            else:
                event.end_date = event.start_date
                event.end_time = None

            event.save()
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'errors': str(e)}, status=400)
    
    return JsonResponse({'status': 'error', 'errors': 'Invalid method'}, status=405)

def subscribe_newsletter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            
            if not email:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Email is required'
                }, status=400)

            # Check if subscriber already exists
            if Subscriber.objects.filter(email=email).exists():
                return JsonResponse({
                    'status': 'error',
                    'message': 'You are already subscribed!'
                }, status=400)

            # Create new subscriber
            subscriber = Subscriber.objects.create(
                email=email,
                is_active=True
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Thank you for subscribing!'
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method'
    }, status=405)

def admission(request):
    return render(request, 'admission.html')

def submit_admission(request):
    if request.method == 'POST':
        try:
            admission = Admission.objects.create(
                full_name=request.POST.get('full_name'),
                email=request.POST.get('email'),
                date_of_birth=request.POST.get('date_of_birth'),
                gender=request.POST.get('gender'),
                phone=request.POST.get('phone'),
                address=request.POST.get('address'),
                
                # Academic Information
                applying_for_grade=request.POST.get('applying_for_grade'),
                previous_school=request.POST.get('previous_school'),
                previous_grade=request.POST.get('previous_grade'),
                previous_percentage=request.POST.get('previous_percentage'),
                
                # Parent Information
                father_name=request.POST.get('father_name'),
                father_occupation=request.POST.get('father_occupation'),
                father_phone=request.POST.get('father_phone'),
                mother_name=request.POST.get('mother_name'),
                mother_occupation=request.POST.get('mother_occupation'),
                mother_phone=request.POST.get('mother_phone'),
                
                # Documents
                student_photo=request.FILES.get('student_photo'),
                previous_marksheet=request.FILES.get('previous_marksheet'),
                transfer_certificate=request.FILES.get('transfer_certificate'),
            )
            
            return JsonResponse({
                'status': 'success',
                'application_id': admission.application_id
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
        
    request.session['admission_email'] = admission.email
    request.session['success_message'] = 'Your application has been submitted successfully!'
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)

def admission_success(request):
    return render(request, 'admission_success.html')