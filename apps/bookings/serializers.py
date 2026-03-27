from rest_framework import serializers
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Booking
from apps.schedules.models import FlightSchedule, TrainSchedule, BusSchedule


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    ticket_pnr = serializers.SerializerMethodField(read_only=True)
    ticket_type = serializers.SerializerMethodField(read_only=True)
    source = serializers.SerializerMethodField(read_only=True)
    destination = serializers.SerializerMethodField(read_only=True)
    journey_date = serializers.SerializerMethodField(read_only=True)
    journey_time = serializers.SerializerMethodField(read_only=True)
    passenger_name = serializers.SerializerMethodField(read_only=True)
    passenger_age = serializers.SerializerMethodField(read_only=True)
    passenger_gender = serializers.SerializerMethodField(read_only=True)
    contact_number = serializers.SerializerMethodField(read_only=True)
    contact_email = serializers.SerializerMethodField(read_only=True)
    base_fare = serializers.SerializerMethodField(read_only=True)
    taxes = serializers.SerializerMethodField(read_only=True)
    
    # Schedule information
    schedule_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Booking
        fields = [
            'id', 'ticket', 'ticket_pnr', 'ticket_type', 'source', 'destination',
            'journey_date', 'journey_time', 'passenger_name', 'passenger_age', 'passenger_gender',
            'contact_number', 'contact_email', 'base_fare', 'taxes',
            'schedule_type', 'schedule_details',
            'number_of_seats', 'booking_status', 'payment_status',
            'total_amount', 'razorpay_order_id', 'razorpay_payment_id', 'booked_at', 'updated_at'
        ]
        read_only_fields = ['id', 'booked_at', 'updated_at']
    
    def get_ticket_pnr(self, obj):
        """Safely get ticket PNR"""
        if obj.ticket:
            return obj.ticket.pnr
        return None
    
    def get_ticket_type(self, obj):
        """Safely get ticket type"""
        if obj.ticket:
            return obj.ticket.ticket_type
        return obj.schedule_type
    
    def get_source(self, obj):
        """Safely get source from ticket or schedule"""
        if obj.ticket:
            return obj.ticket.source
        # Fallback to schedule
        if obj.schedule_type == 'FLIGHT' and obj.flight_schedule:
            return obj.flight_schedule.departure_airport
        elif obj.schedule_type == 'TRAIN' and obj.train_schedule:
            return obj.train_schedule.source_station
        elif obj.schedule_type == 'BUS' and obj.bus_schedule:
            return obj.bus_schedule.boarding_point
        return None
    
    def get_destination(self, obj):
        """Safely get destination from ticket or schedule"""
        if obj.ticket:
            return obj.ticket.destination
        # Fallback to schedule
        if obj.schedule_type == 'FLIGHT' and obj.flight_schedule:
            return obj.flight_schedule.arrival_airport
        elif obj.schedule_type == 'TRAIN' and obj.train_schedule:
            return obj.train_schedule.destination_station
        elif obj.schedule_type == 'BUS' and obj.bus_schedule:
            return obj.bus_schedule.dropping_point
        return None
    
    def get_journey_date(self, obj):
        """Safely get journey date from ticket or schedule"""
        if obj.ticket:
            return obj.ticket.journey_date
        # Fallback to schedule
        if obj.schedule_type == 'FLIGHT' and obj.flight_schedule:
            return obj.flight_schedule.journey_date
        elif obj.schedule_type == 'TRAIN' and obj.train_schedule:
            return obj.train_schedule.journey_date
        elif obj.schedule_type == 'BUS' and obj.bus_schedule:
            return obj.bus_schedule.journey_date
        return None

    def get_journey_time(self, obj):
        """Safely get journey time from ticket (not stored on schedule in this serializer)."""
        if obj.ticket:
            return obj.ticket.journey_time
        # Fallback to schedule
        if obj.schedule_type == 'FLIGHT' and obj.flight_schedule:
            return obj.flight_schedule.departure_time
        elif obj.schedule_type == 'TRAIN' and obj.train_schedule:
            return obj.train_schedule.departure_time
        elif obj.schedule_type == 'BUS' and obj.bus_schedule:
            return obj.bus_schedule.departure_time
        return None
    
    def get_passenger_name(self, obj):
        """Safely get passenger name from ticket or user"""
        if obj.ticket:
            return obj.ticket.passenger_name
        # Fallback to user
        return obj.user.get_full_name() or obj.user.username

    def get_passenger_age(self, obj):
        if obj.ticket:
            return obj.ticket.passenger_age
        return None

    def get_passenger_gender(self, obj):
        if obj.ticket:
            return obj.ticket.passenger_gender
        return None

    def get_contact_number(self, obj):
        if obj.ticket:
            return obj.ticket.contact_number
        phone = getattr(obj.user, 'phone', '') or ''
        return phone or None

    def get_contact_email(self, obj):
        if obj.ticket:
            return obj.ticket.contact_email
        return obj.user.email or None

    def get_base_fare(self, obj):
        if obj.ticket:
            return obj.ticket.base_fare
        # Fallback to schedule
        if obj.schedule_type == 'FLIGHT' and obj.flight_schedule:
            return obj.flight_schedule.base_fare
        elif obj.schedule_type == 'TRAIN' and obj.train_schedule:
            return obj.train_schedule.base_fare
        elif obj.schedule_type == 'BUS' and obj.bus_schedule:
            return obj.bus_schedule.base_fare
        return None

    def get_taxes(self, obj):
        if obj.ticket:
            return obj.ticket.taxes
        # Fallback to schedule
        if obj.schedule_type == 'FLIGHT' and obj.flight_schedule:
            return obj.flight_schedule.taxes
        elif obj.schedule_type == 'TRAIN' and obj.train_schedule:
            return obj.train_schedule.taxes
        elif obj.schedule_type == 'BUS' and obj.bus_schedule:
            return obj.bus_schedule.taxes
        return None
    
    def get_schedule_details(self, obj):
        """Get schedule details based on schedule type"""
        if obj.schedule_type == 'FLIGHT' and obj.flight_schedule:
            return {
                'id': obj.flight_schedule.id,
                'flight_number': obj.flight_schedule.flight_number,
                'airline_name': obj.flight_schedule.airline_name,
                'departure': obj.flight_schedule.departure_airport,
                'arrival': obj.flight_schedule.arrival_airport,
            }
        elif obj.schedule_type == 'TRAIN' and obj.train_schedule:
            return {
                'id': obj.train_schedule.id,
                'train_number': obj.train_schedule.train_number,
                'train_name': obj.train_schedule.train_name,
                'source': obj.train_schedule.source_station,
                'destination': obj.train_schedule.destination_station,
            }
        elif obj.schedule_type == 'BUS' and obj.bus_schedule:
            return {
                'id': obj.bus_schedule.id,
                'bus_number': obj.bus_schedule.bus_number,
                'bus_operator': obj.bus_schedule.bus_operator,
                'boarding': obj.bus_schedule.boarding_point,
                'dropping': obj.bus_schedule.dropping_point,
            }
        return None


class BookingCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new booking from a schedule"""
    schedule_id = serializers.IntegerField(write_only=True)
    number_of_seats = serializers.IntegerField(min_value=1, default=1)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'schedule_type', 'schedule_id', 'number_of_seats', 'total_amount'
        ]
    
    def validate(self, data):
        schedule_type = data.get('schedule_type')
        schedule_id = data.get('schedule_id')
        number_of_seats = data.get('number_of_seats', 1)
        
        if not schedule_type or not schedule_id:
            raise serializers.ValidationError("Schedule type and schedule ID are required")
        
        # Validate schedule exists and has available seats
        try:
            if schedule_type == 'FLIGHT':
                schedule = FlightSchedule.objects.get(pk=schedule_id)
            elif schedule_type == 'TRAIN':
                schedule = TrainSchedule.objects.get(pk=schedule_id)
            elif schedule_type == 'BUS':
                schedule = BusSchedule.objects.get(pk=schedule_id)
            else:
                raise serializers.ValidationError("Invalid schedule type")
            
            # Check availability
            if schedule.available_seats < number_of_seats:
                raise serializers.ValidationError(
                    f"Only {schedule.available_seats} seats available"
                )
            
            if not schedule.is_active or schedule.is_cancelled:
                raise serializers.ValidationError("Schedule is not available for booking")

            departure_at = datetime.combine(schedule.journey_date, schedule.departure_time)
            if timezone.is_naive(departure_at):
                departure_at = timezone.make_aware(departure_at)
            if departure_at <= timezone.now() + timedelta(hours=6):
                raise serializers.ValidationError(
                    "Booking closed: departure is in the past or within 6 hours"
                )
            
            # Store schedule in validated_data for later use
            data['_schedule'] = schedule
            
            # Calculate total amount
            total_fare = float(schedule.base_fare) + float(schedule.taxes)
            data['total_amount'] = total_fare * number_of_seats
            
        except (FlightSchedule.DoesNotExist, TrainSchedule.DoesNotExist, BusSchedule.DoesNotExist):
            raise serializers.ValidationError("Schedule not found")
        
        return data
    
    def create(self, validated_data):
        user = self.context['request'].user
        schedule = validated_data.pop('_schedule')
        schedule_type = validated_data.pop('schedule_type')
        number_of_seats = validated_data.pop('number_of_seats', 1)
        total_amount = validated_data.pop('total_amount', None)
        
        # Remove schedule_id from validated_data (not a Booking model field)
        validated_data.pop('schedule_id', None)
        
        # Create booking with schedule reference
        booking = Booking.objects.create(
            user=user,
            schedule_type=schedule_type,
            number_of_seats=number_of_seats,
            total_amount=total_amount or 0
        )
        
        # Set the appropriate schedule foreign key
        if schedule_type == 'FLIGHT':
            booking.flight_schedule = schedule
        elif schedule_type == 'TRAIN':
            booking.train_schedule = schedule
        elif schedule_type == 'BUS':
            booking.bus_schedule = schedule
        
        booking.save()
        
        return booking
