from rest_framework import serializers
from .models import FoodItem, FoodOrder, OrderItem


class FoodItemSerializer(serializers.ModelSerializer):
    """Serializer for FoodItem model"""
    
    class Meta:
        model = FoodItem
        fields = ['id', 'name', 'description', 'food_type', 'meal_type', 'price', 'is_available', 'image', 'preparation_time']


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model"""
    food_item_name = serializers.CharField(source='food_item.name', read_only=True)
    food_item_price = serializers.DecimalField(source='food_item.price', max_digits=8, decimal_places=2, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'food_item', 'food_item_name', 'food_item_price', 'quantity', 'special_instructions', 'subtotal']


class FoodOrderSerializer(serializers.ModelSerializer):
    """Serializer for FoodOrder model"""
    items = OrderItemSerializer(many=True, read_only=True)
    pnr = serializers.CharField(source='booking.ticket.pnr', read_only=True)
    
    class Meta:
        model = FoodOrder
        fields = [
            'id', 'pnr', 'delivery_station', 'delivery_time', 'seat/coach_info',
            'total_amount', 'status', 'payment_status', 'items', 'ordered_at'
        ]


class FoodOrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a new food order"""
    items = serializers.ListField(child=serializers.DictField())
    
    class Meta:
        model = FoodOrder
        fields = ['booking', 'delivery_station', 'seat/coach_info', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        
        # Calculate total amount
        total_amount = 0
        for item_data in items_data:
            food_item = FoodItem.objects.get(id=item_data['food_item'])
            quantity = item_data.get('quantity', 1)
            total_amount += food_item.price * quantity
        
        # Create food order
        food_order = FoodOrder.objects.create(
            user=user,
            total_amount=total_amount,
            **validated_data
        )
        
        # Create order items
        for item_data in items_data:
            OrderItem.objects.create(food_order=food_order, **item_data)
        
        return food_order
