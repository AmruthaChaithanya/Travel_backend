from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PaymentTransaction
from .razorpay import create_razorpay_order, verify_payment_signature
from apps.bookings.models import Booking


class CreateOrderView(APIView):
    """API endpoint to create Razorpay order"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        amount = request.data.get('amount')
        booking_id = request.data.get('booking_id')
        
        if not amount:
            return Response(
                {'error': 'Amount is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            amount = float(amount)
        except ValueError:
            return Response(
                {'error': 'Invalid amount'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create Razorpay order
        order_id, order = create_razorpay_order(amount)
        
        if not order_id:
            return Response(
                {'error': 'Failed to create payment order'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Create payment transaction record
        transaction = PaymentTransaction.objects.create(
            user=request.user,
            transaction_type='PAYMENT',
            amount=amount,
            status='PENDING',
            razorpay_order_id=order_id,
            booking_id=booking_id if booking_id else None,
            description=f'Payment for booking {booking_id}' if booking_id else 'Payment'
        )
        
        return Response({
            'order_id': order_id,
            'amount': amount,
            'currency': 'INR',
            'key': settings.RAZORPAY_KEY_ID
        })


class VerifyPaymentView(APIView):
    """API endpoint to verify Razorpay payment"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        order_id = request.data.get('razorpay_order_id')
        payment_id = request.data.get('razorpay_payment_id')
        signature = request.data.get('razorpay_signature')
        
        if not all([order_id, payment_id, signature]):
            return Response(
                {'error': 'Missing payment details'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify payment signature
        is_valid = verify_payment_signature(order_id, payment_id, signature)
        
        if not is_valid:
            return Response(
                {'error': 'Invalid payment signature'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Update transaction record
        try:
            transaction = PaymentTransaction.objects.get(
                razorpay_order_id=order_id,
                user=request.user
            )
            transaction.razorpay_payment_id = payment_id
            transaction.razorpay_signature = signature
            transaction.status = 'SUCCESS'
            transaction.save()
            
            # Update booking if exists
            if transaction.booking:
                booking = transaction.booking
                booking.confirm_booking()
            
        except PaymentTransaction.DoesNotExist:
            return Response(
                {'error': 'Transaction not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response({
            'message': 'Payment verified successfully',
            'payment_id': payment_id,
            'status': 'SUCCESS'
        })


class PaymentHistoryView(generics.ListAPIView):
    """API endpoint to get user's payment history"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PaymentTransaction.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        # Manual serialization since we don't have a serializer yet
        data = [{
            'id': t.id,
            'transaction_type': t.transaction_type,
            'amount': str(t.amount),
            'status': t.status,
            'razorpay_order_id': t.razorpay_order_id,
            'razorpay_payment_id': t.razorpay_payment_id,
            'description': t.description,
            'created_at': t.created_at.isoformat()
        } for t in queryset]
        
        return Response(data)
