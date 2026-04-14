from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema
from .models import Restaurant, Table
from .serializers import (
    RestaurantSerializer, RestaurantListSerializer, TableSerializer
)
from .filters import RestaurantFilter, TableFilter
from users.permissions import IsOwner, IsOwnerOrReadOnly


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    ViewSet — CRUD uchun barcha methodlar bitta class'da:
    list()    → GET  /restaurants/
    create()  → POST /restaurants/
    retrieve()→ GET  /restaurants/{id}/
    update()  → PUT  /restaurants/{id}/
    destroy() → DELETE /restaurants/{id}/
    """
    queryset = Restaurant.objects.filter(is_active=True).select_related('owner')
    # select_related — JOIN qiladi, alohida query yubormaslik uchun (performance)

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = RestaurantFilter
    search_fields = ['name', 'address', 'description']
    ordering_fields = ['name', 'rating', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """
        Action'ga qarab serializer tanlash.
        list — yengil serializer (table'larsiz)
        boshqa — to'liq serializer
        """
        if self.action == 'list':
            return RestaurantListSerializer
        return RestaurantSerializer

    def get_permissions(self):
        """
        Action'ga qarab permission tanlash.
        Bu DRF'ning kuchli xususiyati — har bir action uchun alohida permission.
        """
        if self.action in ['list', 'retrieve']:
            # O'qish — hamma, hatto tizimga kirmagan ham
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action == 'create':
            # Yaratish — faqat owner
            permission_classes = [IsOwner]
        else:
            # Update, Delete — faqat o'z restoraning egasi
            permission_classes = [IsOwnerOrReadOnly]
        return [p() for p in permission_classes]

    def perform_create(self, serializer):
        """
        Save paytida owner'ni avtomatik qo'shamiz.
        Foydalanuvchi request'da owner yubormasin — xavfsizlik uchun.
        """
        serializer.save(owner=self.request.user)

    @extend_schema(summary="Restoranning barcha stollarini ko'rish")
    @action(detail=True, methods=['get'], url_path='tables')
    def tables(self, request, pk=None):
        """GET /api/restaurants/{id}/tables/"""
        restaurant = self.get_object()
        tables = restaurant.tables.all()

        # filter parametrlari
        capacity = request.query_params.get('min_capacity')
        if capacity:
            tables = tables.filter(capacity__gte=capacity)

        serializer = TableSerializer(tables, many=True)
        return Response(serializer.data)

    @extend_schema(summary="O'zim egasi bo'lgan restoranlar")
    @action(detail=False, methods=['get'], url_path='my-restaurants',
            permission_classes=[IsOwner])
    def my_restaurants(self, request):
        """GET /api/restaurants/my-restaurants/"""
        restaurants = Restaurant.objects.filter(owner=request.user)
        serializer = RestaurantListSerializer(restaurants, many=True)
        return Response(serializer.data)


class TableViewSet(viewsets.ModelViewSet):
    """Stollarni boshqarish — faqat owner o'z stollarini boshqaradi"""
    queryset = Table.objects.select_related('restaurant', 'restaurant__owner')
    serializer_class = TableSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TableFilter

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticatedOrReadOnly()]
        return [IsOwner()]

    def get_queryset(self):
        """
        URL'da restaurant_id bo'lsa — o'sha restoranning stollarini qaytaradi.
        Nested URL uchun: /api/restaurants/{restaurant_id}/tables/
        """
        queryset = super().get_queryset()
        restaurant_id = self.kwargs.get('restaurant_pk')
        if restaurant_id:
            queryset = queryset.filter(restaurant_id=restaurant_id)
        return queryset