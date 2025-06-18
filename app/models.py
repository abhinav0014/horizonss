from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Notice(models.Model):
    NOTICE_TYPES = (
        ('GENERAL', 'General Notice'),
        ('IMPORTANT', 'Important Notice'),
    )

    title = models.CharField(max_length=200)
    content = models.TextField()
    notice_type = models.CharField(max_length=10, choices=NOTICE_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.email

class Event(models.Model):
    EVENT_TYPES = (
        ('ACADEMIC', 'Academic Event'),
        ('CULTURAL', 'Cultural Event'),
        ('SPORTS', 'Sports Event'),
        ('OTHER', 'Other Event'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=10, choices=EVENT_TYPES)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        return timezone.now().date() <= self.date

    @property
    def is_past(self):
        return timezone.now().date() > self.date
