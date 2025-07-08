from rest_framework import serializers
from .models import Event, Ticket
from .services import generate_seats_for_event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'location', 'date', 'price',
            'total_rows', 'seats_per_row'
        ]
        read_only_fields = ['created_by']
    def create(self, validated_data):
        event = super().create(validated_data)
        generate_seats_for_event(event)
        return event

class TicketSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = ['id', 'purchased_at', 'event']
