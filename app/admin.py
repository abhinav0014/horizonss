from django.contrib import admin
from .models import Notice, Event, Subscriber, Admission

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'notice_type', 'author', 'created_at')
    list_filter = ('notice_type', 'created_at', 'author')
    search_fields = ('title', 'content')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'date', 'time', 'venue', 'is_active')
    list_filter = ('event_type', 'date', 'is_active')
    search_fields = ('title', 'description', 'venue')
    date_hierarchy = 'date'

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('email', 'name')
    date_hierarchy = 'created_at'
    list_per_page = 20
    
    actions = ['activate_subscribers', 'deactivate_subscribers']
    
    def activate_subscribers(self, request, queryset):
        queryset.update(is_active=True)
    activate_subscribers.short_description = "Mark selected subscribers as active"
    
    def deactivate_subscribers(self, request, queryset):
        queryset.update(is_active=False)
    deactivate_subscribers.short_description = "Mark selected subscribers as inactive"

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('application_id', 'full_name', 'applying_for_grade', 'status', 'applied_at')
    list_filter = ('status', 'applying_for_grade', 'applied_at')
    search_fields = ('application_id', 'full_name', 'email', 'phone')
    readonly_fields = ('application_id', 'applied_at', 'updated_at')
    date_hierarchy = 'applied_at'