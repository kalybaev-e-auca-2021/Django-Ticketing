from django.urls import path

from Ticketing.Payment.views import PurchaseWithBalanceView

urlpatterns = [
    path('purchase/<int:event_id>/', PurchaseWithBalanceView.as_view(), name='test-payment-intent'),
]