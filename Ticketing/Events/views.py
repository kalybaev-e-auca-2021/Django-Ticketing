from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from .models import Event, Ticket
from .serializers import EventSerializer, TicketSerializer
from Ticketing.Identity.permissions import IsAdmin, IsUser


@api_view(['GET', 'POST'])
def events_view(request):
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        if not request.user or not request.user.groups.filter(name='ADMIN').exists():
            return Response({'detail': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return None


@api_view(['POST'])
@permission_classes([IsUser])
def buy_event(request, id):
    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

    ticket, created = Ticket.objects.get_or_create(user=request.user, event=event)
    if not created:
        return Response({"message": "You have already bought this event"}, status=status.HTTP_400_BAD_REQUEST)

    return Response({"message": "Event bought successfully"}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsUser])
def my_tickets(request):
    tickets = Ticket.objects.filter(user=request.user).select_related('event')
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)