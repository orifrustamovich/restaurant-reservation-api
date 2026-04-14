from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Nima uchun AbstractUser extend qilamiz?
    Django'ning default User modelida username, password, email bor.
    Biz unga ROLE qo'shmoqchimiz — customer yoki owner.
    AbstractUser bilan barcha default funksiyani saqlab, qo'shimcha field qo'shiladi.
    """

    class Role(models.TextChoices):
        # TextChoices — enum o'rniga ishlatiladi, DB'da string saqlanadi
        CUSTOMER = 'customer', 'Customer'
        OWNER = 'owner', 'Restaurant Owner'
        ADMIN = 'admin', 'Admin'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )
    phone = models.CharField(max_length=20, blank=True)

    # email ni unique qilamiz — login uchun ishlatamiz
    email = models.EmailField(unique=True)

    # USERNAME_FIELD — login qilishda nima ishlatilishini belgilaydi
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS — createsuperuser da so'raladigan fieldlar
    REQUIRED_FIELDS = ['username', 'role']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    # Helper property — template yoki serializer'da is_owner deb tekshirish mumkin
    @property
    def is_owner(self):
        return self.role == self.Role.OWNER

    @property
    def is_customer(self):
        return self.role == self.Role.CUSTOMER


