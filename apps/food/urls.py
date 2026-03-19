from django.urls import path
from .views import (
    FoodMenuView,
    FoodOrderListView,
    CreateFoodOrderView,
    FoodOrderDetailView,
)

urlpatterns = [
    path('menu/', FoodMenuView.as_view(), name='food-menu'),
    path('orders/', FoodOrderListView.as_view(), name='food-order-list'),
    path('orders/create/', CreateFoodOrderView.as_view(), name='food-order-create'),
    path('orders/<int:pk>/', FoodOrderDetailView.as_view(), name='food-order-detail'),
]
