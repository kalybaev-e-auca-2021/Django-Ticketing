from django.urls import path
from .views import buy_event, events_view, my_tickets

urlpatterns = [
    path('events/', events_view, name='events'),
    path('events/<int:id>/buy/', buy_event, name='buy_event'),
    path('my-tickets/', my_tickets, name='my_tickets'),
]
