from rest_framework import serializers
from django.utils import timezone
from .models import Reservation
from restaurants.serializers import TableSerializer, RestaurantListSerializer


class ReservationSerializer(serializers.ModelSerializer):
    """
    Nested serializer — Reservation ichida Table va Restaurant ma'lumoti.
    Bu "read" uchun — ko'rish paytida to'liq ma'lumot.
    """
    # source — modelda qanday fielddan kelishini bildiradi
    table_detail = TableSerializer(source='table', read_only=True)
    restaurant_detail = RestaurantListSerializer(
        source='table.restaurant',
        read_only=True,
    )
    customer_email = serializers.EmailField(source='customer.email', read_only=True)

    class Meta:
        model = Reservation
        fields = [
            'id', 'customer_email', 'table', 'table_detail', 'restaurant_detail',
            'reservation_date', 'start_time', 'end_time', 'party_size',
            'status', 'special_requests', 'created_at',
        ]
        read_only_fields = ['id', 'customer_email', 'status', 'created_at']

    def validate_reservation_date(self, value):
        """O'tib ketgan sanaga bron qilib bo'lmaydi"""
        if value < timezone.now().date():
            raise serializers.ValidationError(
                "O'tib ketgan sanaga bron qilib bo'lmaydi."
            )
        return value

    def validate(self, attrs):
        attrs = super().validate(attrs)

        # Start time end time dan oldin bo'lishi kerak
        if attrs.get('start_time') and attrs.get('end_time'):
            if attrs['start_time'] >= attrs['end_time']:
                raise serializers.ValidationError(
                    "Boshlanish vaqti tugash vaqtidan oldin bo'lishi kerak."
                )

        # =============================
        # CONFLICT CHECK — eng muhim qism
        # =============================
        # Bir stolga bir vaqtda 2 ta bron bo'lmasligi uchun
        table = attrs.get('table')
        date = attrs.get('reservation_date')
        start = attrs.get('start_time')
        end = attrs.get('end_time')

        if table and date and start and end:
            # Mavjud bronlarni tekshiramiz
            # Overlap (kesishish) shartlari:
            #   existing.start < new.end  AND  existing.end > new.start
            # Bu klassik interval kesishish formulasi
            existing_reservations = Reservation.objects.filter(
                table=table,
                reservation_date=date,
                status__in=['pending', 'confirmed'],  # Bekor qilinganlarni hisobga olmaymiz
            ).exclude(
                pk=self.instance.pk if self.instance else None  # Update paytida o'zini exclude qilamiz
            )

            for reservation in existing_reservations:
                overlap = (
                        reservation.start_time < end
                        and reservation.end_time > start
                )
                if overlap:
                    raise serializers.ValidationError(
                        f"Bu stol {reservation.start_time}—{reservation.end_time} "
                        f"vaqtida allaqachon band. Boshqa vaqt tanlang."
                    )

        # Stol sig'imi tekshirish
        if table and attrs.get('party_size'):
            if attrs['party_size'] > table.capacity:
                raise serializers.ValidationError(
                    f"Bu stolga maksimum {table.capacity} kishi sig'adi. "
                    f"Siz {attrs['party_size']} kishi uchun bron qilmoqchisiz."
                )

        return attrs


class ReservationCreateSerializer(serializers.ModelSerializer):
    """
    Create uchun — customer o'zi belgilanadi, status default.
    Nima uchun alohida serializer?
    Create da customer = request.user avtomatik qo'shiladi.
    """

    class Meta:
        model = Reservation
        fields = [
            'table', 'reservation_date', 'start_time', 'end_time',
            'party_size', 'special_requests',
        ]

    # ReservationSerializer'dagi validate metodlarini ko'chiramiz
    validate_reservation_date = ReservationSerializer.validate_reservation_date
    validate = ReservationSerializer.validate