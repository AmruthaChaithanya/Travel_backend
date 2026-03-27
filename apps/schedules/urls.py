from django.urls import path
from .views import (
    FlightScheduleListView,
    FlightScheduleDetailView,
    TrainScheduleListView,
    TrainScheduleDetailView,
    BusScheduleListView,
    BusScheduleDetailView,
    CheckAvailabilityView,
)

urlpatterns = [
    # Flight schedules
    path('flights/', FlightScheduleListView.as_view(), name='flight-schedule-list'),
    path('flights/<int:pk>/', FlightScheduleDetailView.as_view(), name='flight-schedule-detail'),
    
    # Train schedules
    path('trains/', TrainScheduleListView.as_view(), name='train-schedule-list'),
    path('trains/<int:pk>/', TrainScheduleDetailView.as_view(), name='train-schedule-detail'),
    
    # Bus schedules
    path('buses/', BusScheduleListView.as_view(), name='bus-schedule-list'),
    path('buses/<int:pk>/', BusScheduleDetailView.as_view(), name='bus-schedule-detail'),
    
    # Availability check
    path('<str:schedule_type>/<int:pk>/availability/', CheckAvailabilityView.as_view(), name='check-availability'),
]
