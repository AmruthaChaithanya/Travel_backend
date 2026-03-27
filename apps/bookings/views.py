from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer
from .services import calculate_refund_amount, can_cancel_booking


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
    """API endpoint to create a new booking from a schedule"""
    serializer_class = BookingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        booking = serializer.save(user=self.request.user)
        
        # Optionally auto-confirm the booking (can be done after payment)
        # For now, booking is created in PENDING state
        # Call booking.confirm_booking() after successful payment
        
        return booking
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        booking = self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        
        response_data = {
            'message': 'Booking created successfully',
            'booking_id': booking.id,
            'schedule_type': booking.schedule_type,
            'number_of_seats': booking.number_of_seats,
            'total_amount': str(booking.total_amount),
            'booking_status': booking.booking_status,
            'payment_status': booking.payment_status,
            'next_step': 'Confirm booking to generate ticket and PNR'
        }
        
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)


class ConfirmBookingView(APIView):
    """API endpoint to confirm a booking (creates ticket from schedule)"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
        except Booking.DoesNotExist:
            return Response(
                {'error': 'Booking not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if booking.booking_status == 'CONFIRMED':
            return Response(
                {'error': 'Booking already confirmed'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if booking.booking_status == 'CANCELLED':
            return Response(
                {'error': 'Cannot confirm cancelled booking'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Confirm the booking (this will create ticket from schedule)
            passengers = request.data.get('passengers') or []
            contact_details = request.data.get('contact_details') or {}

            primary_passenger = None
            if isinstance(passengers, list) and passengers:
                primary_passenger = passengers[0]
            elif isinstance(passengers, dict):
                primary_passenger = passengers

            booking.confirm_booking(primary_passenger=primary_passenger, contact=contact_details)
            
            return Response({
                'message': 'Booking confirmed successfully',
                'booking_id': booking.id,
                'ticket_pnr': booking.ticket.pnr if booking.ticket else None,
                'booking_status': booking.booking_status,
                'payment_status': booking.payment_status
            })
        except Exception as e:
            # Log the actual error for debugging
            import traceback
            print(f"Error confirming booking: {str(e)}")
            print(traceback.format_exc())
            
            return Response(
                {'error': f'Failed to confirm booking: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


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
        print("Cancel check:", can_cancel, reason)
        if not can_cancel:
            return Response(
                {'error': reason},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Calculate refund
        refund_amount, cancellation_charges, refund_percentage = calculate_refund_amount(booking)
        
        try:
            # Cancel the booking
            booking.cancel_booking()
            
            return Response({
                'message': 'Booking cancelled successfully',
                'refund_amount': str(refund_amount),
                'cancellation_charges': str(cancellation_charges),
                'refund_percentage': refund_percentage
            })
        except Exception as e:
            # Log the actual error for debugging
            import traceback
            print("Error cancelling booking:", str(e))
            print(traceback.format_exc())
            
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
