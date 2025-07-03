from django.urls import path
from .views import EventsView, TicketView

urlpatterns = [
    #GET: list events, POST: create event
    path('events/', EventsView.as_view(), name='events'),

    # POST: buy event ticket
    path('events/<int:event_id>/buy/', TicketView.as_view(), name='buy_event'),

    # GET: view my tickets (user-specific)
    path('my-tickets/', TicketView.as_view(), name='my_tickets'),
]