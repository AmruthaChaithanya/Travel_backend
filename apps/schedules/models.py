from django.db import models
from django.conf import settings


class FlightSchedule(models.Model):
    """Flight Schedule - represents available flights before booking"""
    
    AIRLINE_TYPE = (
        ('DOMESTIC', 'Domestic'),
        ('INTERNATIONAL', 'International'),
    )
    
    SEAT_CLASS = (
        ('ECONOMY', 'Economy'),
        ('BUSINESS', 'Business'),
        ('FIRST', 'First Class'),
    )
    
    airline_name = models.CharField(max_length=100)
    flight_number = models.CharField(max_length=20, unique=True)
    departure_airport = models.CharField(max_length=100)  # Airport code
    arrival_airport = models.CharField(max_length=100)    # Airport code
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    duration = models.CharField(max_length=20)  # e.g., "2h 30m"
    
    journey_date = models.DateField()
    seat_class = models.CharField(max_length=20, choices=SEAT_CLASS)
    airline_type = models.CharField(max_length=20, choices=AIRLINE_TYPE, default='DOMESTIC')
    
    # Capacity management
    total_seats = models.PositiveIntegerField(default=100)
    available_seats = models.PositiveIntegerField(default=100)
    base_fare = models.DecimalField(max_digits=10, decimal_places=2)
    taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_cancelled = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['departure_time', 'journey_date']
    
    def __str__(self):
        return f"{self.flight_number} - {self.departure_airport} to {self.arrival_airport}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate taxes if not set
        if not self.taxes:
            self.taxes = self.base_fare * 0.18  # 18% tax
        super().save(*args, **kwargs)
    
    def decrement_seats(self, count=1):
        """Decrement available seats when booking is made"""
        if self.available_seats >= count:
            self.available_seats -= count
            self.save()
            return True
        return False
    
    def increment_seats(self, count=1):
        """Increment available seats when booking is cancelled"""
        if self.available_seats + count <= self.total_seats:
            self.available_seats += count
            self.save()
            return True
        return False


class TrainSchedule(models.Model):
    """Train Schedule - represents available trains before booking"""
    
    TRAIN_TYPE = (
        ('EXPRESS', 'Express'),
        ('SUPERFAST', 'Superfast'),
        ('PASSENGER', 'Passenger'),
        ('RAJDHANI', 'Rajdhani'),
        ('SHATABDI', 'Shatabdi'),
        ('DURONTO', 'Duronto'),
    )
    
    COACH_CLASS = (
        ('SL', 'Sleeper'),
        ('3A', 'AC 3 Tier'),
        ('2A', 'AC 2 Tier'),
        ('1A', 'AC First Class'),
        ('CC', 'Chair Car'),
        ('2S', 'Second Sitting'),
    )
    
    train_number = models.CharField(max_length=20, unique=True)
    train_name = models.CharField(max_length=100)
    train_type = models.CharField(max_length=20, choices=TRAIN_TYPE)
    
    source_station = models.CharField(max_length=100)  # Station code
    destination_station = models.CharField(max_length=100)  # Station code
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    duration = models.CharField(max_length=20)  # e.g., "12h 30m"
    
    journey_date = models.DateField()
    coach_class = models.CharField(max_length=10, choices=COACH_CLASS)
    
    # Capacity management
    total_seats = models.PositiveIntegerField(default=72)  # Typical coach capacity
    available_seats = models.PositiveIntegerField(default=72)
    base_fare = models.DecimalField(max_digits=10, decimal_places=2)
    taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_cancelled = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['departure_time', 'journey_date']
    
    def __str__(self):
        return f"{self.train_number} - {self.source_station} to {self.destination_station}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate taxes if not set
        if not self.taxes:
            self.taxes = self.base_fare * 0.05  # 5% tax for trains
        super().save(*args, **kwargs)
    
    def decrement_seats(self, count=1):
        """Decrement available seats when booking is made"""
        if self.available_seats >= count:
            self.available_seats -= count
            self.save()
            return True
        return False
    
    def increment_seats(self, count=1):
        """Increment available seats when booking is cancelled"""
        if self.available_seats + count <= self.total_seats:
            self.available_seats += count
            self.save()
            return True
        return False


class BusSchedule(models.Model):
    """Bus Schedule - represents available buses before booking"""
    
    BUS_TYPE = (
        ('AC_SEATER', 'AC Seater'),
        ('NON_AC_SEATER', 'Non-AC Seater'),
        ('AC_SLEEPER', 'AC Sleeper'),
        ('NON_AC_SLEEPER', 'Non-AC Sleeper'),
        ('VOLVO', 'Volvo'),
        ('SCANIA', 'Scania'),
    )
    
    bus_operator = models.CharField(max_length=100)
    bus_number = models.CharField(max_length=20, unique=True)
    bus_type = models.CharField(max_length=20, choices=BUS_TYPE)
    
    boarding_point = models.CharField(max_length=100)
    dropping_point = models.CharField(max_length=100)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    duration = models.CharField(max_length=20)  # e.g., "8h 30m"
    
    journey_date = models.DateField()
    
    # Capacity management
    total_seats = models.PositiveIntegerField(default=40)  # Typical bus capacity
    available_seats = models.PositiveIntegerField(default=40)
    base_fare = models.DecimalField(max_digits=10, decimal_places=2)
    taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_cancelled = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['departure_time', 'journey_date']
    
    def __str__(self):
        return f"{self.bus_number} - {self.boarding_point} to {self.dropping_point}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate taxes if not set
        if not self.taxes:
            self.taxes = self.base_fare * 0.12  # 12% tax for buses
        super().save(*args, **kwargs)
    
    def decrement_seats(self, count=1):
        """Decrement available seats when booking is made"""
        if self.available_seats >= count:
            self.available_seats -= count
            self.save()
            return True
        return False
    
    def increment_seats(self, count=1):
        """Increment available seats when booking is cancelled"""
        if self.available_seats + count <= self.total_seats:
            self.available_seats += count
            self.save()
            return True
        return False
