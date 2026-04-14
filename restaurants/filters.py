import django_filters
from .models import Restaurant, Table


class RestaurantFilter(django_filters.FilterSet):
    """
    URL query parameter orqali filter:
    /api/restaurants/?min_rating=4.0&is_active=true
    """
    min_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='gte')
    max_rating = django_filters.NumberFilter(field_name='rating', lookup_expr='lte')
    # gte = greater than or equal (>=)
    # lte = less than or equal (<=)

    class Meta:
        model = Restaurant
        fields = ['is_active', 'min_rating', 'max_rating']


class TableFilter(django_filters.FilterSet):
    min_capacity = django_filters.NumberFilter(field_name='capacity', lookup_expr='gte')

    class Meta:
        model = Table
        fields = ['restaurant', 'is_available', 'min_capacity']