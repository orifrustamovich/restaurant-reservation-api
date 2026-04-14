from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from users.models import CustomUser
from restaurants.models import Table


class Reservation(models.Model):
    """
    Asosiy business logic shu yerda bo'ladi.
    Conflict check — bir stolga bir vaqtda 2 ta bron bo'lmasligi uchun.
    """

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'  # Kutilmoqda
        CONFIRMED = 'confirmed', 'Confirmed'  # Tasdiqlangan
        CANCELLED = 'cancelled', 'Cancelled'  # Bekor qilingan
        COMPLETED = 'completed', 'Completed'  # Yakunlangan

    customer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='reservations',
    )
    table = models.ForeignKey(
        Table,
        on_delete=models.CASCADE,
        related_name='reservations',
    )

    # Bron boshlanish va tugash vaqti
    reservation_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    party_size = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text='Nechta kishi uchun bron',
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    special_requests = models.TextField(
        blank=True,
        help_text='Maxsus talablar (vegetarian, allergiya va h.k.)',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'
        ordering = ['-reservation_date', '-start_time']

    def __str__(self):
        return (
            f"Reservation #{self.id} — "
            f"{self.customer.email} | "
            f"Table {self.table.table_number} | "
            f"{self.reservation_date} {self.start_time}"
        )

    def is_past(self):
        """Bron o'tib ketganmi?"""
        reservation_datetime = timezone.datetime.combine(
            self.reservation_date,
            self.start_time,
            tzinfo=timezone.get_current_timezone(),
        )
        return reservation_datetime < timezone.now()

    def can_be_cancelled(self):
        """Bekor qilish mumkinmi? Faqat o'tib ketmagan, pending/confirmed bronlar"""
        return (
                not self.is_past()
                and self.status in [self.Status.PENDING, self.Status.CONFIRMED]
        )