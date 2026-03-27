from django.urls import path
from .views import (
    BookingListView,
    BookingDetailView,
    CreateBookingView,
    ConfirmBookingView,
    CancelBookingView,
)

urlpatterns = [
    path('', BookingListView.as_view(), name='booking-list'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('create/', CreateBookingView.as_view(), name='booking-create'),
    path('<int:pk>/confirm/', ConfirmBookingView.as_view(), name='booking-confirm'),
    path('<int:pk>/cancel/', CancelBookingView.as_view(), name='booking-cancel'),
]
