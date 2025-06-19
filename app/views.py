from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from .models import Notice

def home(request):
    return render(request, 'landing.html')


def notices(request):
    return render(request, 'landing.html')


def about(request):
    return render(request, 'landing.html')


def events(request):
    return render(request, 'landing.html')

def contact(request):
    return render(request, 'landing.html')