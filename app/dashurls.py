from django.urls import path
from .dashviews import *

app_name = 'dashboard'

urlpatterns = [
    path('', overview, name='overview'),
    path('notices/', notice_list, name='notices'),
    path('notices/create/', create_notice, name='create_notice'),
    path('notices/edit/<int:notice_id>/', edit_notice, name='edit_notice'),
    path('notices/delete/<int:notice_id>/', delete_notice, name='delete_notice'),
    path('events/', events, name='events'),
    path('events/create/', create_event, name='create_event'),
    path('events/edit/<int:event_id>/', edit_event, name='edit_event'),
    path('events/delete/<int:event_id>/', delete_event, name='delete_event'),
    path('events/toggle-completion/<int:event_id>/', toggle_event_completion, name='toggle_event_completion'),
    path('subscribers/', subscribers, name='subscribers'),
    path('subscribers/export/', export_subscribers, name='export_subscribers'),
    path('subscribers/delete/<int:subscriber_id>/', delete_subscriber, name='delete_subscriber'),
    path('admissions/', admissions, name='admissions'),
    path('admissions/<int:admission_id>/', admission_detail, name='admission_detail'),
    path('admissions/<int:admission_id>/update-status/', update_admission_status, name='update_admission_status'),
    path('faculty/', faculty_management, name='faculty_management'),
    path('faculty/<int:faculty_id>/', faculty_action, name='faculty_action'),
]