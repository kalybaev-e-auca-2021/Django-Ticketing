from django.db import models
from django.conf import settings

class Event(models.Model):
    class Meta:
        db_table = 'identity"."event'

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events_created'
    )

    def __str__(self):
        return self.title

class Ticket(models.Model):
    class Meta:
        db_table = 'identity"."ticket'
        unique_together = ('user', 'event')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} -> {self.event.title}"
