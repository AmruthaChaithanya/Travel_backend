from django.urls import path
from .views import (
    FlightListView,
    FlightDetailView,
    TrainListView,
    TrainDetailView,
    BusListView,
    BusDetailView,
)

urlpatterns = [
    path('flights/', FlightListView.as_view(), name='flight-list'),
    path('flights/<int:pk>/', FlightDetailView.as_view(), name='flight-detail'),
    path('trains/', TrainListView.as_view(), name='train-list'),
    path('trains/<int:pk>/', TrainDetailView.as_view(), name='train-detail'),
    path('buses/', BusListView.as_view(), name='bus-list'),
    path('buses/<int:pk>/', BusDetailView.as_view(), name='bus-detail'),
]
