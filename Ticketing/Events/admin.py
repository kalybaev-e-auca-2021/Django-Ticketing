from django.contrib import admin
from unfold.admin import ModelAdmin

from Ticketing.Events.models import Event


@admin.register(Event)
class EventAdmin(ModelAdmin):
    ordering = ('date',)
    list_display = ('title', 'description')

    fieldsets = (
        (None, {'fields': ('title', 'description')}),
        ('Details', {'fields': ('date', 'price', 'created_by')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('title', 'description', 'date', 'price', 'created_by'),
        }),
    )
    search_fields = ('title', 'description')
