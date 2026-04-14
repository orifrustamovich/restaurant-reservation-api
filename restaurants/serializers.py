from rest_framework import serializers
from .models import Restaurant, Table


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'table_number', 'capacity', 'is_available', 'description']
        read_only_fields = ['id']


class RestaurantSerializer(serializers.ModelSerializer):
    """
    Nested serializer — Restaurant ichida Table listini ko'rsatamiz.
    many=True — bir nechta table bo'lishi mumkin.
    read_only=True — table'larni bu serializer orqali yaratib bo'lmaydi.
    """
    tables = TableSerializer(many=True, read_only=True)
    owner_email = serializers.EmailField(source='owner.email', read_only=True)

    class Meta:
        model = Restaurant
        fields = [
            'id', 'name', 'description', 'address', 'phone', 'email',
            'image', 'opening_time', 'closing_time', 'rating',
            'is_active', 'owner_email', 'tables', 'created_at',
        ]
        read_only_fields = ['id', 'rating', 'created_at', 'owner_email']

    def validate(self, attrs):
        """Opening time closing time dan oldin bo'lishi kerak"""
        if 'opening_time' in attrs and 'closing_time' in attrs:
            if attrs['opening_time'] >= attrs['closing_time']:
                raise serializers.ValidationError(
                    "Ochilish vaqti yopilish vaqtidan oldin bo'lishi kerak."
                )
        return attrs


class RestaurantListSerializer(serializers.ModelSerializer):
    """
    List view uchun — tablelar ko'rsatilmaydi (performance uchun).
    Nima uchun 2 ta serializer?
    List da 100 ta restoran bo'lsa, har birida tablelarni ham qaytarish
    juda ko'p DB so'rovi = sekin API. Shuning uchun list uchun yengil serializer.
    """
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    table_count = serializers.IntegerField(
        source='tables.count',
        read_only=True,
    )

    class Meta:
        model = Restaurant
        fields = [
            'id', 'name', 'address', 'phone', 'opening_time',
            'closing_time', 'rating', 'is_active', 'owner_email', 'table_count',
        ]