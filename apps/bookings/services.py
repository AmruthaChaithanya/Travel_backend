from django.utils import timezone
from datetime import timedelta
from .models import Booking


def calculate_refund_amount(booking):
    """
    Calculate refund amount based on cancellation time
    Returns: (refund_amount, cancellation_charges)
    """
    total_amount = booking.total_amount
    journey_date = booking.ticket.journey_date
    journey_time = booking.ticket.journey_time
    
    # Combine date and time
    journey_datetime = timezone.datetime.combine(journey_date, journey_time)
    journey_datetime = timezone.make_aware(journey_datetime)
    
    current_time = timezone.now()
    hours_before = (journey_datetime - current_time).total_seconds() / 3600
    
    cancellation_charges = 0
    refund_percentage = 0
    
    # Cancellation policy
    if hours_before > 48:
        # More than 48 hours before departure - 10% charges
        cancellation_charges = total_amount * 0.10
        refund_percentage = 90
    elif hours_before > 24:
        # 24-48 hours before departure - 25% charges
        cancellation_charges = total_amount * 0.25
        refund_percentage = 75
    elif hours_before > 12:
        # 12-24 hours before departure - 50% charges
        cancellation_charges = total_amount * 0.50
        refund_percentage = 50
    elif hours_before > 4:
        # 4-12 hours before departure - 75% charges
        cancellation_charges = total_amount * 0.75
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
    
    if booking.ticket.is_cancelled:
        return False, "Ticket already cancelled"
    
    journey_date = booking.ticket.journey_date
    journey_time = booking.ticket.journey_time
    
    journey_datetime = timezone.datetime.combine(journey_date, journey_time)
    journey_datetime = timezone.make_aware(journey_datetime)
    
    current_time = timezone.now()
    hours_before = (journey_datetime - current_time).total_seconds() / 3600
    
    if hours_before <= 0:
        return False, "Cannot cancel after journey departure time"
    
    return True, None
