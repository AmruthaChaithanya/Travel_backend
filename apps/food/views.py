from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FoodItem, FoodOrder
from .serializers import FoodItemSerializer, FoodOrderSerializer, FoodOrderCreateSerializer


class FoodMenuView(generics.ListAPIView):
    """API endpoint to get food menu"""
    serializer_class = FoodItemSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        queryset = FoodItem.objects.filter(is_available=True)
        
        # Filter by meal type
        meal_type = self.request.query_params.get('meal_type')
        if meal_type:
            queryset = queryset.filter(meal_type=meal_type)
        
        # Filter by food type
        food_type = self.request.query_params.get('food_type')
        if food_type:
            queryset = queryset.filter(food_type=food_type)
        
        return queryset


class FoodOrderListView(generics.ListAPIView):
    """API endpoint to get user's food orders"""
    serializer_class = FoodOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return FoodOrder.objects.filter(user=self.request.user)


class CreateFoodOrderView(generics.CreateAPIView):
    """API endpoint to create a new food order"""
    serializer_class = FoodOrderCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class FoodOrderDetailView(generics.RetrieveAPIView):
    """API endpoint to get food order details"""
    serializer_class = FoodOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return FoodOrder.objects.filter(user=self.request.user)
