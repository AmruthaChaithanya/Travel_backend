from django.contrib import admin
from .models import FoodItem, FoodOrder, OrderItem

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'meal_type', 'food_type', 'price', 'is_available']
    list_filter = ['meal_type', 'food_type', 'is_available']
    search_fields = ['name', 'description']


@admin.register(FoodOrder)
class FoodOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'pnr_display', 'delivery_station', 'total_amount', 'status', 'ordered_at']
    list_filter = ['status', 'payment_status']
    search_fields = ['user__username', 'booking__ticket__pnr']
    
    def pnr_display(self, obj):
        return obj.booking.ticket.pnr if obj.booking and obj.booking.ticket else '-'
    pnr_display.short_description = 'PNR'


admin.site.register(OrderItem)
