from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer
from .services import calculate_refund_amount, can_cancel_booking
from apps.payments.razorpay import create_refund_transaction


class BookingListView(generics.ListAPIView):
    """API endpoint to get user's bookings"""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(user=user)


class BookingDetailView(generics.RetrieveAPIView):
    """API endpoint to get booking details"""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class CreateBookingView(generics.CreateAPIView):
    """API endpoint to create a new booking"""
    serializer_class = BookingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)
        # Update ticket status
        if booking.ticket:
            booking.ticket.status = 'PENDING'
            booking.ticket.save()
        return booking


class CancelBookingView(APIView):
    """API endpoint to cancel a booking"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
        except Booking.DoesNotExist:
            return Response(
                {'error': 'Booking not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if booking can be cancelled
        can_cancel, reason = can_cancel_booking(booking)
        if not can_cancel:
            return Response(
                {'error': reason},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate refund
        refund_amount, cancellation_charges, refund_percentage = calculate_refund_amount(booking)
        
        # Cancel the booking
        booking.cancel_booking()
        
        # Create refund transaction if applicable
        if refund_amount > 0:
            create_refund_transaction(
                user=request.user,
                amount=refund_amount,
                original_payment_id=booking.razorpay_payment_id,
                description=f"Refund for cancelled booking {booking.id} - PNR: {booking.ticket.pnr}"
            )
        
        return Response({
            'message': 'Booking cancelled successfully',
            'refund_amount': str(refund_amount),
            'cancellation_charges': str(cancellation_charges),
            'refund_percentage': refund_percentage
        })
