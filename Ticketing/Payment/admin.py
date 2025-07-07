from django.contrib import admin

from unfold.admin import ModelAdmin

from Ticketing.Payment.models import Payment


@admin.register(Payment)
class PaymentAdmin(ModelAdmin):
    ordering = ('user',)
    list_display = ('user', 'amount',)

    fieldsets = (
        (None, {'fields': ('user', 'amount')}),
        ('Info', {'fields': ('status', 'from_balance')}),
    )
