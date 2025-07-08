from Ticketing.Events.models import Seat, Ticket
from Ticketing.Payment.models import Payment


def issue_ticket(user, event, *, payment_method):
    seat = Seat.objects.filter(event=event, is_reserved=False).first()
    if not seat:
        raise Exception("No seats available")
    seat.is_reserved = True
    seat.save()

    payment = Payment.objects.create(
        user=user,
        amount=event.price,
        status='succeeded',
        from_balance=(payment_method == 'balance')
    )

    ticket = Ticket.objects.create(
        user=user,
        event=event,
        seat=seat,
        payment=payment,
    )
    return ticket

def generate_seats_for_event(event):
    for row in range(1, event.total_rows + 1):
        for number in range(1, event.seats_per_row + 1):
            Seat.objects.create(
                event=event,
                row=str(row),
                number=str(number),
                is_reserved=False
            )