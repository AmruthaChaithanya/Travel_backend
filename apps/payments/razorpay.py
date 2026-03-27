import razorpay
from django.conf import settings


razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


def create_razorpay_order(amount, currency='INR'):
    """
    Create a Razorpay order.
    amount is in rupees; Razorpay expects paise.
    """
    order_data = {
        'amount': int(float(amount) * 100),
        'currency': currency,
        'payment_capture': 1,
    }
    order = razorpay_client.order.create(data=order_data)
    return order['id'], order


def verify_payment_signature(order_id, payment_id, signature):
    razorpay_client.utility.verify_payment_signature(
        {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature,
        }
    )
    return True

