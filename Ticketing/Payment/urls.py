from django.urls import path

from Ticketing.Payment.views import CreateStripePayment

urlpatterns = [
    path('create-payment/', CreateStripePayment.as_view(), name='create-payment'),
]