from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ticket_pnr_display', 'booking_status', 'payment_status', 'total_amount', 'booked_at']
    list_filter = ['booking_status', 'payment_status']
    search_fields = ['user__username', 'ticket__pnr']
    
    def ticket_pnr_display(self, obj):
        return obj.ticket.pnr if obj.ticket else '-'
    ticket_pnr_display.short_description = 'PNR'
