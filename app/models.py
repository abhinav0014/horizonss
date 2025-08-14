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
    image = models.ImageField(upload_to='notices/', blank=True, null=True)  # Add this line
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
    # Keep original fields for backwards compatibility
    date = models.DateField()
    time = models.TimeField()
    # Add new fields with defaults
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(default=timezone.now)
    end_time = models.TimeField(null=True, blank=True)
    venue = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Ensure backwards compatibility
        self.date = self.start_date
        self.time = self.start_time
        if not self.end_date:
            self.end_date = self.start_date
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-start_date', '-start_time']

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        return timezone.now().date() <= self.date and not self.is_completed

    @property
    def is_past(self):
        return timezone.now().date() > self.date or self.is_completed

    def mark_completed(self):
        self.is_completed = True
        self.completed_at = timezone.now()
        self.save()

class Admission(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('REVIEWING', 'Under Review'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected')
    )
    
    # Personal Information
    full_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    
    # Academic Information
    applying_for_grade = models.IntegerField()
    previous_school = models.CharField(max_length=200)
    previous_grade = models.IntegerField()
    previous_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    # Parent/Guardian Information
    father_name = models.CharField(max_length=100)
    father_occupation = models.CharField(max_length=100)
    father_phone = models.CharField(max_length=15)
    mother_name = models.CharField(max_length=100)
    mother_occupation = models.CharField(max_length=100)
    mother_phone = models.CharField(max_length=15)
    
    # Documents
    student_photo = models.ImageField(upload_to='admissions/photos/')
    previous_marksheet = models.FileField(upload_to='admissions/documents/')
    transfer_certificate = models.FileField(upload_to='admissions/documents/')
    
    # Meta Information
    application_id = models.CharField(max_length=10, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.application_id:
            # Generate application ID: ADM + YEAR + Random 4 digits
            import random
            year = timezone.now().strftime('%y')
            random_num = ''.join([str(random.randint(0, 9)) for _ in range(4)])
            self.application_id = f'ADM{year}{random_num}'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.application_id} - {self.full_name}"

    class Meta:
        ordering = ['-applied_at']

class Faculty(models.Model):
    LEVEL_CHOICES = (
        ('NSY', 'Nursery'),
        ('LKG', 'Lower KG'),
        ('UKG', 'Upper KG'),
        ('PRIMARY', 'Primary (1-5)'),
        ('MIDDLE', 'Middle (6-8)'),
        ('SECONDARY', 'Secondary (9-10)'),
        ('PLUS2_SCIENCE', 'Plus 2 Science'),
        ('PLUS2_MANAGEMENT', 'Plus 2 Management'),
        ('PLUS2_EDUCATION', 'Plus 2 Education'),
        ('BACHELOR', 'Bachelor Level')
    )

    DEPARTMENT_CHOICES = (
        ('SCIENCE', 'Science'),
        ('MATHEMATICS', 'Mathematics'),
        ('ENGLISH', 'English'),
        ('NEPALI', 'Nepali'),
        ('SOCIAL', 'Social Studies'),
        ('COMPUTER', 'Computer Science'),
        ('ACCOUNTS', 'Accounts'),
        ('EDUCATION', 'Education'),
        ('OTHER', 'Other')
    )

    # Personal Information
    full_name = models.CharField(max_length=100)
    profile_photo = models.ImageField(upload_to='faculty/photos/', null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    
    # Professional Information
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    teaching_levels = models.JSONField(default=list)  # Add this line if not present
    qualifications = models.TextField()
    experience_years = models.PositiveIntegerField()
    
    # Additional Information
    bio = models.TextField(blank=True)
    specialization = models.CharField(max_length=200, blank=True)
    achievements = models.TextField(blank=True)
    joining_date = models.DateField()
    is_active = models.BooleanField(default=True)
    
    # Social Links
    linkedin = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    website = models.URLField(blank=True)
    
    # Meta Information
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['department', 'full_name']
        verbose_name_plural = 'Faculty Members'

    def __str__(self):
        return f"{self.full_name} - {self.designation}"
