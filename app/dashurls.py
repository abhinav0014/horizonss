from django.urls import path
from .dashviews import *

app_name = 'dashboard'

urlpatterns = [
    path('', overview, name='overview'),
    path('notices/', notice_list, name='notices'),
    path('events/', events, name='events'),
    path('subscribers/', subscribers, name='subscribers'),
    path('subscribers/export/', export_subscribers, name='export_subscribers'),
    path('subscribers/delete/<int:subscriber_id>/', delete_subscriber, name='delete_subscriber'),
]