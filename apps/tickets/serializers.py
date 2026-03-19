from rest_framework import serializers
from .models import Ticket, Flight, Train, Bus


class TicketSerializer(serializers.ModelSerializer):
    """Base serializer for Ticket model"""
    
    class Meta:
        model = Ticket
        fields = [
            'id', 'pnr', 'ticket_type', 'status', 'source', 'destination',
            'journey_date', 'journey_time', 'passenger_name', 'passenger_age',
            'passenger_gender', 'contact_number', 'contact_email', 'base_fare',
            'taxes', 'total_amount', 'booked_at', 'cancelled_at', 'is_cancelled'
        ]
        read_only_fields = ['id', 'pnr', 'booked_at', 'cancelled_at']


class FlightSerializer(serializers.ModelSerializer):
    """Serializer for Flight tickets"""
    
    class Meta:
        model = Flight
        fields = [
            'id', 'pnr', 'status', 'source', 'destination', 'journey_date',
            'journey_time', 'passenger_name', 'passenger_age', 'passenger_gender',
            'contact_number', 'contact_email', 'base_fare', 'taxes', 'total_amount',
            'booked_at', 'airline_name', 'flight_number', 'departure_airport',
            'arrival_airport', 'departure_time', 'arrival_time', 'duration', 'seat_class'
        ]
        read_only_fields = ['id', 'pnr', 'booked_at']


class TrainSerializer(serializers.ModelSerializer):
    """Serializer for Train tickets"""
    
    class Meta:
        model = Train
        fields = [
            'id', 'pnr', 'status', 'source', 'destination', 'journey_date',
            'journey_time', 'passenger_name', 'passenger_age', 'passenger_gender',
            'contact_number', 'contact_email', 'base_fare', 'taxes', 'total_amount',
            'booked_at', 'train_name', 'train_number', 'boarding_station',
            'arrival_station', 'departure_time', 'arrival_time', 'duration',
            'coach', 'seat_number'
        ]
        read_only_fields = ['id', 'pnr', 'booked_at']


class BusSerializer(serializers.ModelSerializer):
    """Serializer for Bus tickets"""
    
    class Meta:
        model = Bus
        fields = [
            'id', 'pnr', 'status', 'source', 'destination', 'journey_date',
            'journey_time', 'passenger_name', 'passenger_age', 'passenger_gender',
            'contact_number', 'contact_email', 'base_fare', 'taxes', 'total_amount',
            'booked_at', 'bus_operator', 'bus_number', 'bus_type', 'boarding_point',
            'dropping_point', 'departure_time', 'arrival_time', 'duration', 'seat_numbers'
        ]
        read_only_fields = ['id', 'pnr', 'booked_at']
