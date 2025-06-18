from django.urls import path, include
from . import views

app_name = 'app'

urlpatterns = [
    path('', views.notice_list, name='notice_list'),
]