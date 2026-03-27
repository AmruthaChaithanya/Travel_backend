from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.bookings.models import Booking
from .models import PaymentTransaction
from .razorpay import create_razorpay_order, verify_payment_signature


class CreateOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        booking_id = request.data.get('booking_id')
        currency = request.data.get('currency') or 'INR'

        if not amount:
            return Response({'error': 'Amount is required'}, status=status.HTTP_400_BAD_REQUEST)
        if not booking_id:
            return Response({'error': 'booking_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            amount = float(amount)
            booking = Booking.objects.get(id=booking_id, user=request.user)
            order_id, _ = create_razorpay_order(amount, currency=currency)
            PaymentTransaction.objects.create(
                user=request.user,
                transaction_type='PAYMENT',
                amount=amount,
                status='PENDING',
                razorpay_order_id=order_id,
                booking=booking,
                description=f'Payment for booking {booking_id}',
            )
            return Response(
                {
                    'order_id': order_id,
                    'amount': int(amount * 100),
                    'currency': currency,
                    'key': 'admin1',
                }
            )
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Failed to create payment order: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyPaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        order_id = request.data.get('razorpay_order_id')
        payment_id = request.data.get('razorpay_payment_id')
        signature = request.data.get('razorpay_signature')
        passengers = request.data.get('passengers') or []
        contact_details = request.data.get('contact_details') or {}

        if not all([order_id, payment_id, signature]):
            return Response({'error': 'Missing payment details'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            transaction = PaymentTransaction.objects.get(razorpay_order_id=order_id, user=request.user)
            verify_payment_signature(order_id, payment_id, signature)

            transaction.razorpay_payment_id = payment_id
            transaction.razorpay_signature = signature
            transaction.status = 'SUCCESS'
            transaction.save()

            booking = transaction.booking
            if booking:
                booking.razorpay_order_id = order_id
                booking.razorpay_payment_id = payment_id
                booking.razorpay_signature = signature
                booking.payment_status = 'PAID'
                booking.save()

                if booking.booking_status != 'CONFIRMED':
                    primary = passengers[0] if isinstance(passengers, list) and passengers else None
                    booking.confirm_booking(primary_passenger=primary, contact=contact_details)
                    booking.refresh_from_db()

            return Response(
                {
                    'message': 'Payment verified successfully',
                    'payment_id': payment_id,
                    'status': 'SUCCESS',
                    'booking_id': booking.id if booking else None,
                    'ticket_pnr': booking.ticket.pnr if booking and booking.ticket else None,
                    'booking_status': booking.booking_status if booking else None,
                }
            )
        except PaymentTransaction.DoesNotExist:
            return Response({'error': 'Transaction not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'Payment verification failed: {e}'}, status=status.HTTP_400_BAD_REQUEST)


class PaymentHistoryView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PaymentTransaction.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        data = [
            {
                'id': t.id,
                'transaction_type': t.transaction_type,
                'amount': str(t.amount),
                'status': t.status,
                'razorpay_order_id': t.razorpay_order_id,
                'razorpay_payment_id': t.razorpay_payment_id,
                'description': t.description,
                'created_at': t.created_at.isoformat(),
            }
            for t in queryset
        ]
        return Response(data)

