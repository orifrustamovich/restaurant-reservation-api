from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import CustomUser


class Restaurant(models.Model):
    """
    Nima uchun owner ForeignKey?
    Bir owner bir nechta restaurant ochishi mumkin (1-to-many).
    on_delete=CASCADE — owner o'chirilsa, uning restoranlari ham o'chadi.
    """
    owner = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='restaurants',  # owner.restaurants.all() deb ishlatish mumkin
        limit_choices_to={'role': 'owner'},  # Faqat owner bo'lgan userlar
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=300)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)

    # ImageField — Pillow kutubxonasi kerak
    image = models.ImageField(
        upload_to='restaurants/',  # media/restaurants/ papkasiga saqlaydi
        null=True,
        blank=True,
    )

    # Ish vaqtlari — oddiy TimeField bilan
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    # Rating — 1 dan 5 gacha
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Restaurant'
        verbose_name_plural = 'Restaurants'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} — {self.owner.email}"

    def is_open_at(self, time):
        """Berilgan vaqtda restoran ochiq ekanligini tekshiradi"""
        return self.opening_time <= time <= self.closing_time


class Table(models.Model):
    """
    Har bir stol restoraniga tegishli.
    table_number — restoranlar ichida unique bo'lishi kerak.
    Misol: "Sushi Place" restoranida 1-stol, "Pizza House" da ham 1-stol bo'lishi mumkin.
    """
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name='tables',
    )
    table_number = models.PositiveIntegerField()
    capacity = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        help_text='Stol sig\'imi (nechta kishi sig\'adi)',
    )
    is_available = models.BooleanField(default=True)
    description = models.CharField(max_length=200, blank=True)

    class Meta:
        verbose_name = 'Table'
        verbose_name_plural = 'Tables'
        # unique_together — bir restoranda bir xil raqamli stol bo'lmasligi uchun
        unique_together = ['restaurant', 'table_number']
        ordering = ['restaurant', 'table_number']

    def __str__(self):
        return f"Table {self.table_number} (cap: {self.capacity}) — {self.restaurant.name}"