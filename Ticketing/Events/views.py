from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Event, Ticket
from .serializers import EventSerializer, TicketSerializer
from Ticketing.Identity.permissions import IsAdmin, IsUser


class EventsView(APIView):
    @permission_classes([IsUser])
    def get(self, request):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @permission_classes([IsAdmin])
    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TicketView(APIView):
    permission_classes = [IsUser]

    def post(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        ticket, created = Ticket.objects.get_or_create(user=request.user, event=event)
        if not created:
            return Response({"message": "You have already bought this event"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Event bought successfully"}, status=status.HTTP_201_CREATED)

    def get(self, request):
        tickets = Ticket.objects.filter(user=request.user).select_related('event')
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
