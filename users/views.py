from rest_framework import generics, status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register/
    Nima uchun generics.CreateAPIView?
    Faqat POST method kerak — CreateAPIView buni avtomatik qiladi.
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]  # Hamma register qila oladi

    @extend_schema(summary="Yangi foydalanuvchi ro'yxatdan o'tkazish")
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Xato bo'lsa 400 qaytaradi
        user = serializer.save()

        # Darhol token ham beramiz — foydalanuvchi login qilmasa ham ishlaydi
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """POST /api/auth/login/"""
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @extend_schema(
        request=LoginSerializer,
        summary="Tizimga kirish va JWT token olish",
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        return Response(
            {
                'user': UserSerializer(data['user']).data,
                'refresh': data['refresh'],
                'access': data['access'],
            }
        )


class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Refresh token'ni blacklist'ga qo'shamiz — boshqa ishlatib bo'lmaydi.
    Access token xali ishlaydi (60 daq), lekin bu normaal.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.Serializer

    @extend_schema(summary="Tizimdan chiqish")
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Muvaffaqiyatli chiqildi."})
        except Exception:
            return Response(
                {"error": "Noto'g'ri token."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ProfileView(generics.RetrieveUpdateAPIView):
    """GET, PUT, PATCH /api/auth/profile/"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # request.user — JWT tokendan aniqlanadi
        return self.request.user