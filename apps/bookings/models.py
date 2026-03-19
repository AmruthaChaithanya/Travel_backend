from django.db import models
from django.conf import settings


class Booking(models.Model):
    """Booking model linking users to tickets"""
    
    BOOKING_STATUS = (
        ('CONFIRMED', 'Confirmed'),
        ('PENDING', 'Pending'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    )
    
    PAYMENT_STATUS = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    ticket = models.ForeignKey('tickets.Ticket', on_delete=models.CASCADE, related_name='bookings')
    
    booking_status = models.CharField(max_length=20, choices=BOOKING_STATUS, default='PENDING')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING')
    
    razorpay_order_id = models.CharField(max_length=255, blank=True)
    razorpay_payment_id = models.CharField(max_length=255, blank=True)
    razorpay_signature = models.CharField(max_length=255, blank=True)
    
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-booked_at']
    
    def __str__(self):
        return f"Booking {self.id} - {self.ticket.pnr} - {self.user.username}"
    
    def confirm_booking(self):
        """Confirm the booking after successful payment"""
        self.booking_status = 'CONFIRMED'
        self.payment_status = 'PAID'
        if self.ticket:
            self.ticket.status = 'CONFIRMED'
            self.ticket.save()
        self.save()
    
    def cancel_booking(self):
        """Cancel the booking"""
        self.booking_status = 'CANCELLED'
        if self.ticket and not self.ticket.is_cancelled:
            self.ticket.cancel()
        self.save()
