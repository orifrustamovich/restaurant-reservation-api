from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import RegisterView, LoginView, LogoutView, ProfileView
from restaurants.views import RestaurantViewSet, TableViewSet
from reservations.views import ReservationViewSet

# Router — ViewSet'larni avtomatik URL'larga bog'laydi
router = DefaultRouter()
router.register('restaurants', RestaurantViewSet, basename='restaurant')
router.register('tables', TableViewSet, basename='table')
router.register('reservations', ReservationViewSet, basename='reservation')

urlpatterns = [
    # Auth endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),

    # Router bilan yaratilgan URLlar:
    # GET  /api/restaurants/
    # POST /api/restaurants/
    # GET  /api/restaurants/{id}/
    # PUT  /api/restaurants/{id}/
    # ...
    path('', include(router.urls)),
]