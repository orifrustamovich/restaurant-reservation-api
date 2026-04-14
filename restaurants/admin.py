from django.contrib import admin
from .models import Restaurant, Table


class TableInline(admin.TabularInline):
    """Restaurant admin sahifasida Tablelar ham ko'rinsin"""
    model = Table
    extra = 0


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'rating', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'address', 'owner__email']
    inlines = [TableInline]


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['table_number', 'restaurant', 'capacity', 'is_available']
    list_filter = ['is_available', 'restaurant']