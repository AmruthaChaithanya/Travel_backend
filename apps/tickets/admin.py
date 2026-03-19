from django.contrib import admin
from .models import Ticket, Flight, Train, Bus

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['pnr', 'ticket_type', 'status', 'source', 'destination', 'journey_date', 'total_amount']
    list_filter = ['ticket_type', 'status', 'journey_date']
    search_fields = ['pnr', 'passenger_name', 'contact_email']


admin.site.register(Flight)
admin.site.register(Train)
admin.site.register(Bus)
