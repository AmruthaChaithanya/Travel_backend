from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    ticket_pnr = serializers.CharField(source='ticket.pnr', read_only=True)
    ticket_type = serializers.CharField(source='ticket.ticket_type', read_only=True)
    source = serializers.CharField(source='ticket.source', read_only=True)
    destination = serializers.CharField(source='ticket.destination', read_only=True)
    journey_date = serializers.DateField(source='ticket.journey_date', read_only=True)
    passenger_name = serializers.CharField(source='ticket.passenger_name', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'ticket', 'ticket_pnr', 'ticket_type', 'source', 'destination',
            'journey_date', 'passenger_name', 'booking_status', 'payment_status',
            'total_amount', 'razorpay_order_id', 'razorpay_payment_id', 'booked_at', 'updated_at'
        ]
        read_only_fields = ['id', 'booked_at', 'updated_at']


class BookingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new booking"""
    
    class Meta:
        model = Booking
        fields = ['ticket', 'total_amount']
    
    def create(self, validated_data):
        user = self.context['request'].user
        booking = Booking.objects.create(
            user=user,
            **validated_data
        )
        return booking
