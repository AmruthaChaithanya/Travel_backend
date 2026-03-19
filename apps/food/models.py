from django.db import models
from django.conf import settings


class FoodItem(models.Model):
    """Food menu items available for train ordering"""
    
    FOOD_TYPE = (
        ('VEG', 'Vegetarian'),
        ('NON_VEG', 'Non-Vegetarian'),
        ('VEGAN', 'Vegan'),
        ('JAIN', 'Jain'),
    )
    
    MEAL_TYPE = (
        ('BREAKFAST', 'Breakfast'),
        ('LUNCH', 'Lunch'),
        ('SNACKS', 'Snacks'),
        ('DINNER', 'Dinner'),
        ('BEVERAGES', 'Beverages'),
    )
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    food_type = models.CharField(max_length=20, choices=FOOD_TYPE)
    meal_type = models.CharField(max_length=20, choices=MEAL_TYPE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='food_images/', null=True, blank=True)
    preparation_time = models.CharField(max_length=50, default='30 mins')
    
    class Meta:
        ordering = ['meal_type', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.price}"


class FoodOrder(models.Model):
    """Food orders placed by users for train journeys"""
    
    ORDER_STATUS = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('PREPARING', 'Preparing'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='food_orders')
    booking = models.ForeignKey('bookings.Booking', on_delete=models.CASCADE, related_name='food_orders')
    
    # Delivery details
    delivery_station = models.CharField(max_length=100)  # Station where food will be delivered
    delivery_time = models.DateTimeField(null=True, blank=True)
    seat_coach_info = models.CharField(max_length=50, blank=True)
    
    # Order details
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='PENDING')
    
    # Payment
    payment_status = models.CharField(max_length=20, default='PENDING')
    razorpay_payment_id = models.CharField(max_length=255, blank=True)
    
    ordered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-ordered_at']
    
    def __str__(self):
        return f"Food Order {self.id} - {self.user.username} - PNR: {self.booking.ticket.pnr if self.booking.ticket else 'N/A'}"


class OrderItem(models.Model):
    """Individual items in a food order"""
    food_order = models.ForeignKey(FoodOrder, on_delete=models.CASCADE, related_name='items')
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    special_instructions = models.TextField(blank=True)
    
    @property
    def subtotal(self):
        return self.food_item.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity}x {self.food_item.name}"
