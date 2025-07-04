from django.contrib import admin
from .models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'date', 'price', 'created_by')
    search_fields = ('title', 'location')

admin.site.register(Event, EventAdmin)