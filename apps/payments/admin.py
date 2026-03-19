from django.contrib import admin
from .models import PaymentTransaction

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'transaction_type', 'amount', 'status', 'razorpay_payment_id', 'created_at']
    list_filter = ['transaction_type', 'status']
    search_fields = ['user__username', 'razorpay_order_id', 'razorpay_payment_id']
