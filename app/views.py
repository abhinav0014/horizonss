from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import Notice

def is_admin(user):
    return user.is_superuser

def notice_list(request):
    notices = Notice.objects.all()
    return render(request, 'app/notice_list.html', {'notices': notices})

# @user_passes_test(is_admin)
# def create_notice(request):
#     # Add form handling logic here
#     pass

# @user_passes_test(is_admin)
def dashboard(request):
    notices = Notice.objects.all()[:5]  # Get last 5 notices
    return render(request, 'dashboard.html', {
        'notices': notices,
    })
