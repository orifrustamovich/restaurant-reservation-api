from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['email', 'username', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active']
    search_fields = ['email', 'username']

    # UserAdmin'ning default fieldset'iga role qo'shamiz
    fieldsets = UserAdmin.fieldsets + (
        ('Qo\'shimcha', {'fields': ['role', 'phone']}),
    )