from django.db import models
from django.utils.crypto import get_random_string


class Ticket(models.Model):
    """Base Ticket model for all types of bookings"""
    
    STATUS_CHOICES = (
        ('CONFIRMED', 'Confirmed'),
        ('WAITING', 'Waiting List'),
        ('CANCELLED', 'Cancelled'),
        ('PENDING', 'Pending'),
    )
    
    TICKET_TYPE = (
        ('FLIGHT', 'Flight'),
        ('TRAIN', 'Train'),
        ('BUS', 'Bus'),
    )
    
    pnr = models.CharField(max_length=10, unique=True, editable=False)
    ticket_type = models.CharField(max_length=10, choices=TICKET_TYPE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    # Journey details
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    journey_date = models.DateField()
    journey_time = models.TimeField()
    
    # Passenger details
    passenger_name = models.CharField(max_length=200)
    passenger_age = models.IntegerField()
    passenger_gender = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=15)
    contact_email = models.EmailField()
    
    # Pricing
    base_fare = models.DecimalField(max_digits=10, decimal_places=2)
    taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Booking metadata
    booked_at = models.DateTimeField(auto_now_add=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    is_cancelled = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-booked_at']
    
    def __str__(self):
        return f"{self.pnr} - {self.ticket_type}"
    
    def save(self, *args, **kwargs):
        if not self.pnr:
            self.pnr = self.generate_pnr()
        super().save(*args, **kwargs)
    
    @staticmethod
    def generate_pnr():
        """Generate a unique 10-digit PNR number"""
        import random
        import string
        return ''.join(random.choices(string.digits, k=10))
    
    def cancel(self):
        """Cancel the ticket"""
        self.is_cancelled = True
        self.status = 'CANCELLED'
        self.cancelled_at = timezone.now()
        self.save()


class Flight(Ticket):
    """Flight-specific ticket details"""
    
    airline_name = models.CharField(max_length=100)
    flight_number = models.CharField(max_length=20)
    departure_airport = models.CharField(max_length=100)
    arrival_airport = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    duration = models.CharField(max_length=20)  # e.g., "2h 30m"
    seat_class = models.CharField(max_length=50)  # Economy, Business, First Class
    
    class Meta:
        db_table = 'tickets_flight'


class Train(Ticket):
    """Train-specific ticket details"""
    
    train_name = models.CharField(max_length=100)
    train_number = models.CharField(max_length=20)
    boarding_station = models.CharField(max_length=100)
    arrival_station = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    duration = models.CharField(max_length=20)
    coach = models.CharField(max_length=20)  # Sleeper, AC, etc.
    seat_number = models.CharField(max_length=20, blank=True)
    
    class Meta:
        db_table = 'tickets_train'


class Bus(Ticket):
    """Bus-specific ticket details"""
    
    bus_operator = models.CharField(max_length=100)
    bus_number = models.CharField(max_length=20)
    bus_type = models.CharField(max_length=50)  # AC, Non-AC, Sleeper, Seater
    boarding_point = models.CharField(max_length=100)
    dropping_point = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    duration = models.CharField(max_length=20)
    seat_numbers = models.CharField(max_length=100)  # Comma-separated seat numbers
    
    class Meta:
        db_table = 'tickets_bus'
