from django.urls import path
from .views import *

app_name = 'app'

urlpatterns = [
    path('', home, name='home'),
    path('events/', events, name='events'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    # path('gallery/', gallery, name='gallery'),
    
    path('notices/', notices, name='notices'),
    # path('notices/<int:notice_id>/', notice_detail, name='notice_detail'),
    path('subscribe-newsletter/', subscribe_newsletter, name='subscribe_newsletter'),
    path('admission/', admission, name='admission'),
    path('admission/submit/', submit_admission, name='submit_admission'),
    path('admission/success/', admission_success, name='admission_success'),
]