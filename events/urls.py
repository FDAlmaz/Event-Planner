from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('event/<int:event_id>/register/', views.register_for_event, name='register_event'),
    path('my-events/', views.my_events, name='my_events'),
    path('register/', views.register, name='register'),
]