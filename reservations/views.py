from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from drf_spectacular.utils import extend_schema
from .models import Reservation
from .serializers import ReservationSerializer, ReservationCreateSerializer
from .filters import ReservationFilter
from users.permissions import IsReservationOwner


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.select_related(
        'customer', 'table', 'table__restaurant'
    )
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = ReservationFilter
    ordering_fields = ['reservation_date', 'created_at']
    ordering = ['-reservation_date']

    def get_serializer_class(self):
        if self.action == 'create':
            return ReservationCreateSerializer
        return ReservationSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'retrieve']:
            return [IsAuthenticated(), IsReservationOwner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Admin — hamma bronlarni ko'radi.
        Oddiy foydalanuvchi — faqat o'zinikini.
        """
        user = self.request.user
        if user.is_staff:
            return super().get_queryset()
        return super().get_queryset().filter(customer=user)

    def perform_create(self, serializer):
        """Customer avtomatik qo'shiladi"""
        serializer.save(customer=self.request.user)

    @extend_schema(summary="Bronni bekor qilish")
    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        """
        POST /api/reservations/{id}/cancel/
        Business logic:
        1. Faqat o'z bronini bekor qila oladi
        2. O'tib ketgan bronni bekor qilib bo'lmaydi
        3. Allaqachon bekor qilinganini qayta bekor qilib bo'lmaydi
        """
        reservation = self.get_object()

        if not reservation.can_be_cancelled():
            if reservation.is_past():
                return Response(
                    {"error": "O'tib ketgan bronni bekor qilib bo'lmaydi."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"error": f"'{reservation.status}' statusidagi bronni bekor qilib bo'lmaydi."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reservation.status = Reservation.Status.CANCELLED
        reservation.save(update_fields=['status', 'updated_at'])
        # update_fields — faqat shu fieldlarni DB'ga yozadi, tezroq ishlaydi

        return Response(
            {
                "message": "Bron muvaffaqiyatli bekor qilindi.",
                "reservation": ReservationSerializer(reservation).data,
            }
        )

    @extend_schema(summary="Bronni tasdiqlash — faqat restoran egasi")
    @action(detail=True, methods=['post'], url_path='confirm')
    def confirm(self, request, pk=None):
        """POST /api/reservations/{id}/confirm/"""
        reservation = self.get_object()

        # Faqat bu restoranning egasi tasdiqlay oladi
        if not request.user.is_staff:
            restaurant_owner = reservation.table.restaurant.owner
            if restaurant_owner != request.user:
                return Response(
                    {"error": "Faqat restoran egasi bron tasdiqlaydi."},
                    status=status.HTTP_403_FORBIDDEN,
                )

        if reservation.status != Reservation.Status.PENDING:
            return Response(
                {"error": "Faqat 'pending' statusidagi bron tasdiqlanadi."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reservation.status = Reservation.Status.CONFIRMED
        reservation.save(update_fields=['status', 'updated_at'])

        return Response({"message": "Bron tasdiqlandi.", "status": "confirmed"})