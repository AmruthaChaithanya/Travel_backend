import razorpay
from django.conf import settings
from apps.accounts.models import Transaction


# Initialize Razorpay client
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


def create_razorpay_order(amount, currency='INR'):
    """
    Create a Razorpay order
    :param amount: Amount in paise (1 INR = 100 paise)
    :param currency: Currency code (default: INR)
    :return: Order ID
    """
    try:
        order_data = {
            'amount': int(amount * 100),  # Convert to paise
            'currency': currency,
            'payment_capture': 1  # Auto-capture payments
        }
        order = razorpay_client.order.create(data=order_data)
        return order['id'], order
    except Exception as e:
        print(f"Error creating Razorpay order: {str(e)}")
        return None, None


def verify_payment_signature(order_id, payment_id, signature):
    """
    Verify Razorpay payment signature
    :param order_id: Razorpay order ID
    :param payment_id: Razorpay payment ID
    :param signature: Razorpay signature
    :return: True if valid, False otherwise
    """
    try:
        razorpay_client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })
        return True
    except Exception as e:
        print(f"Payment verification failed: {str(e)}")
        return False


def fetch_payment_details(payment_id):
    """
    Fetch payment details from Razorpay
    :param payment_id: Razorpay payment ID
    :return: Payment details dict
    """
    try:
        payment = razorpay_client.payment.fetch(payment_id)
        return payment
    except Exception as e:
        print(f"Error fetching payment details: {str(e)}")
        return None


def create_refund_transaction(user, amount, original_payment_id, description):
    """
    Create a refund transaction record
    Note: Actual refund needs to be processed through Razorpay dashboard or API
    """
    try:
        transaction = Transaction.objects.create(
            user=user,
            transaction_type='REFUND',
            amount=amount,
            status='SUCCESS',
            razorpay_payment_id=original_payment_id,
            description=description
        )
        return transaction
    except Exception as e:
        print(f"Error creating refund transaction: {str(e)}")
        return None
