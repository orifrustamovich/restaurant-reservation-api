from django.contrib import admin
from .models import Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'customer', 'get_restaurant', 'table',
        'reservation_date', 'start_time', 'status'
    ]
    list_filter = ['status', 'reservation_date']
    search_fields = ['customer__email', 'table__restaurant__name']
    readonly_fields = ['created_at', 'updated_at']

    # Custom column — related field dan ma'lumot
    @admin.display(description='Restaurant')
    def get_restaurant(self, obj):
        return obj.table.restaurant.name