from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Faqat restaurant owner uchun ruxsat.
    Nima uchun BasePermission extend qilamiz?
    DRF permission tizimi has_permission() methodini tekshiradi.
    """
    message = "Bu amalni faqat restoran egasi bajarishi mumkin."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_owner
        )


class IsCustomer(BasePermission):
    """Faqat customer uchun ruxsat."""
    message = "Bu amalni faqat mijoz bajarishi mumkin."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.is_customer
        )


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission:
    - O'qish (GET) — hammaga
    - Yozish (POST/PUT/DELETE) — faqat owner'ga
    has_object_permission — faqat bitta object'ga permission tekshiradi
    """
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        # obj.owner — restaurant'ning egasi
        return obj.owner == request.user


class IsReservationOwner(BasePermission):
    """
    Faqat o'z bronini ko'ra/o'zgartira oladi.
    Admin esa hammani ko'ra oladi.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.customer == request.user