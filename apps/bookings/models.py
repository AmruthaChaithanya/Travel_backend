from django.db import models
from django.conf import settings


class Booking(models.Model):
    """Booking model linking users to tickets and schedules"""
    
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
    
    VEHICLE_TYPE = (
        ('FLIGHT', 'Flight'),
        ('TRAIN', 'Train'),
        ('BUS', 'Bus'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    ticket = models.ForeignKey('tickets.Ticket', on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    
    # Link to schedule (before ticket is created)
    schedule_type = models.CharField(max_length=10, choices=VEHICLE_TYPE, null=True, blank=True)
    flight_schedule = models.ForeignKey('schedules.FlightSchedule', on_delete=models.SET_NULL, null=True, blank=True)
    train_schedule = models.ForeignKey('schedules.TrainSchedule', on_delete=models.SET_NULL, null=True, blank=True)
    bus_schedule = models.ForeignKey('schedules.BusSchedule', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Booking details
    number_of_seats = models.PositiveIntegerField(default=1)
    
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
        pnr = self.ticket.pnr if self.ticket else "No Ticket"
        return f"Booking {self.id} - {pnr} - {self.user.username}"
    
    def _resolve_passenger_contact(self, primary_passenger=None, contact=None):
        """Map passenger form + contact form (from payment verify) onto ticket fields."""
        p = primary_passenger if isinstance(primary_passenger, dict) else {}
        c = contact if isinstance(contact, dict) else {}
        name = (p.get("name") or "").strip() or (self.user.get_full_name() or self.user.username)
        try:
            age = int(p.get("age"))
        except (TypeError, ValueError):
            age = 25
        gender = (p.get("gender") or "OTHER").upper()[:10]
        if gender not in ("MALE", "FEMALE", "OTHER"):
            gender = "OTHER"
        phone = (c.get("phone") or getattr(self.user, "phone", "") or "").strip() or "N/A"
        phone = phone[:15]
        email = (c.get("email") or self.user.email or "").strip() or "unknown@example.com"
        return name, age, gender, phone, email

    def confirm_booking(self, primary_passenger=None, contact=None):
        """Confirm the booking after successful payment and create ticket from schedule"""
        try:
            from apps.tickets.models import Flight, Train, Bus
            
            self.booking_status = 'CONFIRMED'
            self.payment_status = 'PAID'
            
            # Create ticket from schedule if not already created
            if not self.ticket and self.schedule_type:
                ticket = self._create_ticket_from_schedule(
                    primary_passenger=primary_passenger, contact=contact
                )
                if ticket:
                    self.ticket = ticket
            
            if self.ticket:
                self.ticket.status = 'CONFIRMED'
                self.ticket.save()
            
            self.save()
        except Exception as e:
            print(f"Error in confirm_booking: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
    
    def _create_ticket_from_schedule(self, primary_passenger=None, contact=None):
        """Create a ticket from the selected schedule"""
        # Use absolute import with full path
        from apps.tickets.models import Flight, Train, Bus

        pname, page, pgender, pphone, pemail = self._resolve_passenger_contact(
            primary_passenger, contact
        )
        
        if self.schedule_type == 'FLIGHT' and self.flight_schedule:
            schedule = self.flight_schedule
            ticket = Flight.objects.create(
                pnr=Flight.generate_pnr(),
                ticket_type='FLIGHT',
                status='PENDING',
                source=schedule.departure_airport,
                destination=schedule.arrival_airport,
                journey_date=schedule.journey_date,
                journey_time=schedule.departure_time,
                passenger_name=pname,
                passenger_age=page,
                passenger_gender=pgender,
                contact_number=pphone,
                contact_email=pemail,
                base_fare=schedule.base_fare,
                taxes=schedule.taxes,
                total_amount=self.total_amount,
                airline_name=schedule.airline_name,
                flight_number=schedule.flight_number,
                departure_airport=schedule.departure_airport,
                arrival_airport=schedule.arrival_airport,
                departure_time=schedule.departure_time,
                arrival_time=schedule.arrival_time,
                duration=schedule.duration,
                seat_class=schedule.seat_class,
            )
            # Decrement seats from schedule
            schedule.decrement_seats(self.number_of_seats)
            return ticket
            
        elif self.schedule_type == 'TRAIN' and self.train_schedule:
            schedule = self.train_schedule
            ticket = Train.objects.create(
                pnr=Train.generate_pnr(),
                ticket_type='TRAIN',
                status='PENDING',
                source=schedule.source_station,
                destination=schedule.destination_station,
                journey_date=schedule.journey_date,
                journey_time=schedule.departure_time,
                passenger_name=pname,
                passenger_age=page,
                passenger_gender=pgender,
                contact_number=pphone,
                contact_email=pemail,
                base_fare=schedule.base_fare,
                taxes=schedule.taxes,
                total_amount=self.total_amount,
                train_name=schedule.train_name,
                train_number=schedule.train_number,
                boarding_station=schedule.source_station,
                arrival_station=schedule.destination_station,
                departure_time=schedule.departure_time,
                arrival_time=schedule.arrival_time,
                duration=schedule.duration,
                coach=schedule.coach_class,
            )
            # Decrement seats from schedule
            schedule.decrement_seats(self.number_of_seats)
            return ticket
            
        elif self.schedule_type == 'BUS' and self.bus_schedule:
            schedule = self.bus_schedule
            ticket = Bus.objects.create(
                pnr=Bus.generate_pnr(),
                ticket_type='BUS',
                status='PENDING',
                source=schedule.boarding_point,
                destination=schedule.dropping_point,
                journey_date=schedule.journey_date,
                journey_time=schedule.departure_time,
                passenger_name=pname,
                passenger_age=page,
                passenger_gender=pgender,
                contact_number=pphone,
                contact_email=pemail,
                base_fare=schedule.base_fare,
                taxes=schedule.taxes,
                total_amount=self.total_amount,
                bus_operator=schedule.bus_operator,
                bus_number=schedule.bus_number,
                bus_type=schedule.bus_type,
                boarding_point=schedule.boarding_point,
                dropping_point=schedule.dropping_point,
                departure_time=schedule.departure_time,
                arrival_time=schedule.arrival_time,
                duration=schedule.duration,
                seat_numbers='',  # Should be assigned based on availability
            )
            # Decrement seats from schedule
            schedule.decrement_seats(self.number_of_seats)
            return ticket
        
        return None
    
    def cancel_booking(self):
        """Cancel the booking and restore seats to schedule"""
        self.booking_status = 'CANCELLED'

        # Fix: the previous condition was logically inverted and prevented
        # ticket cancellation + seat restoration in many cases.
        ticket_was_cancelled = False
        if self.ticket:
            ticket_was_cancelled = getattr(self.ticket, 'is_cancelled', False) or (
                getattr(self.ticket, 'status', None) == 'CANCELLED'
            )

            if hasattr(self.ticket, 'cancel') and not ticket_was_cancelled:
                self.ticket.cancel()
            elif not ticket_was_cancelled:
                self.ticket.status = 'CANCELLED'
                self.ticket.save()

            # Restore seats back to schedule only if we actually cancelled
            # the ticket in this operation.
            if not ticket_was_cancelled:
                self._restore_seats_to_schedule()
        
        self.save()
    
    def _restore_seats_to_schedule(self):
        """Restore seats back to the schedule when booking is cancelled"""
        if self.schedule_type == 'FLIGHT' and self.flight_schedule:
            self.flight_schedule.increment_seats(self.number_of_seats)
        elif self.schedule_type == 'TRAIN' and self.train_schedule:
            self.train_schedule.increment_seats(self.number_of_seats)
        elif self.schedule_type == 'BUS' and self.bus_schedule:
            self.bus_schedule.increment_seats(self.number_of_seats)
