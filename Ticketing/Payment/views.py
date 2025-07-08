import json

import stripe
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from Ticketing.Events.models import Event, Ticket, Seat
from Ticketing.Payment.models import Payment

def issue_ticket(user, event, *, payment_method):
    seat = Seat.objects.filter(event=event, is_reserved=False).first()
    if not seat:
        raise Exception("No seats available")
    seat.is_reserved = True
    seat.save()

    ticket = Ticket.objects.create(
        user=user,
        event=event,
        seat=seat,
    )

    Payment.objects.create(
        user=user,
        amount=event.price,
        status='succeeded',
        from_balance=(payment_method == 'balance')
    )
    return ticket

class CreateStripePayment(APIView):
    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        user = request.user
        event = Event.objects.get(id=data['event_id'])
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=int(event.price*100),
                currency='usd',
                payment_method_types=['card'],
                confirm=True,
                payment_method='pm_card_visa',
            )
            ticket = issue_ticket(user, event, payment_method='stripe')
            return JsonResponse({'status': 'success', 'payment_intent': payment_intent})
        except stripe.error.StripeError as e:
            return JsonResponse({'status': 'error', 'message': str(e)})