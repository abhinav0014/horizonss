from django import forms
from .models import Event, Notice

class EventForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Event
        fields = ['title', 'description', 'event_type', 'date', 'time', 'venue', 'is_active']

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'content', 'notice_type', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4}),
        }