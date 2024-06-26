from django.urls import path, include, re_path
from . import views

app_name = 'cal'
urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^calendare/$', views.CalendarView.as_view(), name='calendar'),
    re_path(r'^event/new/$', views.event, name='event_new'),
	re_path(r'^event/edit/(?P<event_id>\d+)/$', views.event, name='event_edit'),
]
