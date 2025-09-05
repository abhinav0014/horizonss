from django.contrib.auth import views as auth_views
from django.contrib.auth import password_validation
from django.urls import path, reverse_lazy
from .views import *

app_name = 'app'

# Password reset URLs with enhanced configuration
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
    path('faculty/', faculty_list, name='faculty_list'),
    path('faculty/<int:faculty_id>/', faculty_detail, name='faculty_detail'),
    path('programs/', programs, name='programs'),


    path('admin/login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='admin_login'),
    path('admin/logout/', auth_views.LogoutView.as_view(next_page='home', http_method_names=['get', 'post']), name='admin_logout'),
    
    # Password reset URLs with enhanced configuration
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='admin/password_reset.html',
             email_template_name='admin/password_reset_email.html',  # Plain text version
             html_email_template_name='admin/password_reset_email_html.html',  # HTML version
             subject_template_name='admin/password_reset_subject.txt',
             success_url=reverse_lazy('app:password_reset_done'),
             extra_context={
                 'site_name': 'New Horizon School',
                 'site_domain': 'newhorizon.edu.np'
             }
         ), 
         name='password_reset'),
    
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='admin/password_reset_done.html',
             extra_context={
                 'site_name': 'New Horizon School'
             }
         ), 
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='admin/password_reset_confirm.html',
             success_url=reverse_lazy('app:password_reset_complete'),
             form_class=auth_views.SetPasswordForm,
             extra_context={
                 'password_validators_help_texts': password_validation.password_validators_help_texts(),
                 'site_name': 'New Horizon School'
             }
         ), 
         name='password_reset_confirm'),
    
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='admin/password_reset_complete.html',
             extra_context={
                 'site_name': 'New Horizon School'
             }
         ), 
         name='password_reset_complete'),
    path('admission/download/<str:application_id>/', download_admission_pdf, name='download_admission_pdf'),
]