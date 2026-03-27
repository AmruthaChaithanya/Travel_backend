from django.utils import timezone
from datetime import timedelta
from .models import Booking
from decimal import Decimal
from datetime import datetime


def _get_journey_datetime(booking):
    """Resolve journey datetime from ticket, else from selected schedule."""
    if booking.ticket:
        journey_date = booking.ticket.journey_date
        journey_time = booking.ticket.journey_time
    elif booking.schedule_type == 'FLIGHT' and booking.flight_schedule:
        journey_date = booking.flight_schedule.journey_date
        journey_time = booking.flight_schedule.departure_time
    elif booking.schedule_type == 'TRAIN' and booking.train_schedule:
        journey_date = booking.train_schedule.journey_date
        journey_time = booking.train_schedule.departure_time
    elif booking.schedule_type == 'BUS' and booking.bus_schedule:
        journey_date = booking.bus_schedule.journey_date
        journey_time = booking.bus_schedule.departure_time
    else:
        return None

    journey_datetime = datetime.combine(journey_date, journey_time)
    if timezone.is_naive(journey_datetime):
        journey_datetime = timezone.make_aware(journey_datetime)
    return journey_datetime

def calculate_refund_amount(booking):
    def calculate_refund_amount(booking):
        print("Updated function")
    """
    Calculate refund amount based on cancellation time
    Returns: (refund_amount, cancellation_charges)
    """
    total_amount = booking.total_amount
    journey_datetime = _get_journey_datetime(booking)
    if not journey_datetime:
        # If journey metadata is missing, do not crash cancellation flow.
        return Decimal('0'), total_amount, 0
    
    current_time = timezone.now()
    hours_before = (journey_datetime - current_time).total_seconds() / 3600
    
    cancellation_charges = Decimal('0')
    refund_percentage = 0
    
    # Cancellation policy
    if hours_before > 48:
        # More than 48 hours before departure - 10% charges
        cancellation_charges = total_amount* Decimal('0.10')
        refund_percentage = 90
    elif hours_before > 24:
        # 24-48 hours before departure - 25% charges
        cancellation_charges = total_amount * Decimal('0.25')
        refund_percentage = 75
    elif hours_before > 12:
        # 12-24 hours before departure - 50% charges
        cancellation_charges = total_amount * Decimal('0.50')
        refund_percentage = 50
    elif hours_before > 4:
        # 4-12 hours before departure - 75% charges
        cancellation_charges = total_amount * Decimal('0.75')
        refund_percentage = 25
    else:
        # Less than 4 hours - No refund
        cancellation_charges = total_amount
        refund_percentage = 0
    
    refund_amount = total_amount - cancellation_charges
    
    return refund_amount, cancellation_charges, refund_percentage


def can_cancel_booking(booking):
    """
    Check if a booking can be cancelled
    Returns: (can_cancel, reason)
    """
    if booking.booking_status == 'CANCELLED':
        return False, "Booking already cancelled"
    
    if booking.ticket and booking.ticket.is_cancelled:
        return False, "Ticket already cancelled"

    journey_datetime = _get_journey_datetime(booking)
    if not journey_datetime:
        return False, "Journey details unavailable for this booking"
    
    current_time = timezone.now()
    hours_before = (journey_datetime - current_time).total_seconds() / 3600
    
    if hours_before <= 0:
        return False, "Cannot cancel after journey departure time"
    
    return True, None
