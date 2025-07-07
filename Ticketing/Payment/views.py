from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from Ticketing.Events.models import Event, Ticket
from Ticketing.Payment.models import Payment


def issue_ticket(user, event, *, payment_method):
    ticket = Ticket.objects.create(user=user, event=event)

    creator = event.created_by
    creator.balance += event.price
    creator.save()

    Payment.objects.create(
        user=user,
        amount=event.price,
        status='succeeded',
        from_balance=(payment_method == 'balance')
    )
    return ticket

class PurchaseWithBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, event_id):
        try:
            event = Event.objects.get(id=event_id)
            user = request.user

            if user.balance < event.price:
                return Response({'error': 'Insufficient balance'}, status=400)

            user.balance -= event.price
            user.save()

            ticket = issue_ticket(user, event, payment_method='balance')

            return Response({
                'message': 'Ticket purchased successfully',
                'ticket_id': ticket.id,
                'new_balance': user.balance
            }, status=201)

        except Event.DoesNotExist:
            return Response({'error': 'Event not found'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
