from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    """
    Nima uchun ModelSerializer?
    Model fieldlarini avtomatik oladi, validate qiladi, save() qiladi.
    password — write_only, chunki javobda ko'rsatmaslik kerak.
    """
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'},  # Swagger'da password field bo'ladi
    )
    password2 = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
    )

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'password', 'password2', 'role', 'phone']
        extra_kwargs = {
            'role': {'required': True},
        }

    def validate(self, attrs):
        """
        Cross-field validation — bir nechta fieldni birgalikda tekshirish.
        super().validate() — parent class validatsiyasini ham bajaradi.
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Parollar mos kelmadi."})
        return attrs

    def create(self, validated_data):
        # password2 ni olib tashlaymiz — model'da bunday field yo'q
        validated_data.pop('password2')
        # create_user — parolni hash qiladi (muhim!)
        user = CustomUser.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Nima uchun ModelSerializer emas?
    Login — model bilan bog'liq emas, faqat email va parol kerak.
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs['email'],  # USERNAME_FIELD=email bo'lgani uchun
            password=attrs['password'],
        )
        if not user:
            raise serializers.ValidationError("Email yoki parol noto'g'ri.")
        if not user.is_active:
            raise serializers.ValidationError("Foydalanuvchi bloklangan.")

        # Token yaratamiz
        refresh = RefreshToken.for_user(user)
        return {
            'user': user,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class UserSerializer(serializers.ModelSerializer):
    """Profile ko'rish uchun — parol ko'rinmasin"""

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'role', 'phone', 'date_joined']
        read_only_fields = ['id', 'date_joined']