from django.contrib import admin
from unfold.admin import ModelAdmin

from Ticketing.Events.models import Event, Ticket, Country, City, Location


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
            'fields': ('title', 'description', 'date', 'price', 'location', 'created_by' ),
        }),
    )
    search_fields = ('title', 'description')


@admin.register(Ticket)
class TicketAdmin(ModelAdmin):
    ordering = ('purchased_at',)
    list_display = ('user', 'event')

    fieldsets = (
        (None, {'fields': ('user', 'event', 'payment')}),
    )

@admin.register(Country)
class CountryAdmin(ModelAdmin):
    ordering = ('name',)
    list_display = ('name', 'code')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'code'),
        }),
    )

@admin.register(City)
class CityAdmin(ModelAdmin):
    ordering = ('name',)
    list_display = ('name', 'country')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'country'),
        }),
    )

@admin.register(Location)
class LocationAdmin(ModelAdmin):
    ordering = ('name',)
    list_display = ('name',)

    fieldsets = (
        (None, {'fields': ('name',)}),
        ('Details', {'fields': ('address', 'city')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name', 'address', 'city'),
        }),
    )