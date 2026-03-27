from django.contrib import admin
from .models import FlightSchedule, TrainSchedule, BusSchedule


@admin.register(FlightSchedule)
class FlightScheduleAdmin(admin.ModelAdmin):
    list_display = ['flight_number', 'airline_name', 'departure_airport', 'arrival_airport', 
                    'journey_date', 'departure_time', 'available_seats', 'total_seats', 'base_fare']
    list_filter = ['airline_name', 'journey_date', 'seat_class', 'is_active']
    search_fields = ['flight_number', 'airline_name', 'departure_airport', 'arrival_airport']
    ordering = ['journey_date', 'departure_time']


@admin.register(TrainSchedule)
class TrainScheduleAdmin(admin.ModelAdmin):
    list_display = ['train_number', 'train_name', 'source_station', 'destination_station',
                    'journey_date', 'departure_time', 'available_seats', 'total_seats', 'base_fare']
    list_filter = ['train_type', 'coach_class', 'journey_date', 'is_active']
    search_fields = ['train_number', 'train_name', 'source_station', 'destination_station']
    ordering = ['journey_date', 'departure_time']


@admin.register(BusSchedule)
class BusScheduleAdmin(admin.ModelAdmin):
    list_display = ['bus_number', 'bus_operator', 'boarding_point', 'dropping_point',
                    'journey_date', 'departure_time', 'available_seats', 'total_seats', 'base_fare']
    list_filter = ['bus_type', 'bus_operator', 'journey_date', 'is_active']
    search_fields = ['bus_number', 'bus_operator', 'boarding_point', 'dropping_point']
    ordering = ['journey_date', 'departure_time']
