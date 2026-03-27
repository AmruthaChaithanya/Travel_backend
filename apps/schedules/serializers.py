from rest_framework import serializers
from .models import FlightSchedule, TrainSchedule, BusSchedule


class FlightScheduleSerializer(serializers.ModelSerializer):
    """Serializer for Flight Schedule"""
    
    total_fare = serializers.SerializerMethodField()
    
    class Meta:
        model = FlightSchedule
        fields = [
            'id', 'airline_name', 'flight_number', 'departure_airport', 'arrival_airport',
            'departure_time', 'arrival_time', 'duration', 'journey_date', 'seat_class',
            'airline_type', 'total_seats', 'available_seats', 'base_fare', 'taxes',
            'total_fare', 'is_active', 'is_cancelled'
        ]
        read_only_fields = ['id', 'is_active']
    
    def get_total_fare(self, obj):
        return float(obj.base_fare) + float(obj.taxes)


class TrainScheduleSerializer(serializers.ModelSerializer):
    """Serializer for Train Schedule"""
    
    total_fare = serializers.SerializerMethodField()
    
    class Meta:
        model = TrainSchedule
        fields = [
            'id', 'train_number', 'train_name', 'train_type', 'source_station',
            'destination_station', 'departure_time', 'arrival_time', 'duration',
            'journey_date', 'coach_class', 'total_seats', 'available_seats',
            'base_fare', 'taxes', 'total_fare', 'is_active', 'is_cancelled'
        ]
        read_only_fields = ['id', 'is_active']
    
    def get_total_fare(self, obj):
        return float(obj.base_fare) + float(obj.taxes)


class BusScheduleSerializer(serializers.ModelSerializer):
    """Serializer for Bus Schedule"""
    
    total_fare = serializers.SerializerMethodField()
    
    class Meta:
        model = BusSchedule
        fields = [
            'id', 'bus_operator', 'bus_number', 'bus_type', 'boarding_point',
            'dropping_point', 'departure_time', 'arrival_time', 'duration',
            'journey_date', 'total_seats', 'available_seats', 'base_fare',
            'taxes', 'total_fare', 'is_active', 'is_cancelled'
        ]
        read_only_fields = ['id', 'is_active']
    
    def get_total_fare(self, obj):
        return float(obj.base_fare) + float(obj.taxes)
