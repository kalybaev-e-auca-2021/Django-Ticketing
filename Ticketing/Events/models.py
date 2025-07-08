from django.db import models
from django.conf import settings

from Ticketing.Payment.models import Payment


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.ForeignKey('Location', on_delete=models.CASCADE, related_name='events')
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_rows = models.IntegerField(default=0)
    seats_per_row = models.IntegerField(default=0)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events_created'
    )
    created_at = models.DateTimeField(auto_now_add=True,  null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title

class Seat(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='seats')
    row = models.CharField(max_length=10)
    number = models.CharField(max_length=10)
    is_reserved = models.BooleanField(default=False)

class Ticket(models.Model):
    class Meta:
        unique_together = ('user', 'event')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True, blank=True)
    seat = models.ForeignKey(Seat, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} -> {self.event.title}"

class Country(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')

    class Meta:
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='locations')
    address = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name