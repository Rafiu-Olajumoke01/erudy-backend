import uuid
from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils import timezone

from tenants.models import School
from applications.models import Application


class PromoCode(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='promo_codes',
    )
    code = models.CharField(max_length=30)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=15)
    is_active = models.BooleanField(default=True)
    valid_until = models.DateTimeField(null=True, blank=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='promo_codes_created',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('school', 'code')

    def __str__(self):
        return f"{self.code} ({self.school.name})"

    @property
    def is_valid(self):
        if not self.is_active:
            return False
        if self.valid_until and timezone.now() > self.valid_until:
            return False
        return True


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        AWAITING_CONFIRMATION = "awaiting_confirmation", "Awaiting Confirmation"
        PAID = "paid", "Paid"
        EXPIRED = "expired", "Expired"
        FAILED = "failed", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='payments',
    )
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='payments',
    )
    promo_code = models.ForeignKey(
        PromoCode,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='payments',
    )

    tx_ref = models.CharField(max_length=100, unique=True, editable=False)

    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Amount expected, after any promo discount")
    confirmed_amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    status = models.CharField(max_length=30, choices=Status.choices, default=Status.PENDING)

    payment_proof = models.ImageField(upload_to='payment_proofs/', blank=True, null=True)
    student_reference_note = models.CharField(
        max_length=255, blank=True,
        help_text="Optional note from student, e.g. their bank transfer reference"
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='payments_reviewed',
    )
    reviewed_at = models.DateTimeField(blank=True, null=True)

    expires_at = models.DateTimeField()
    paid_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=30)
        if not self.tx_ref:
            self.tx_ref = f"HUB-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)

    @property
    def is_expired(self):
        active_statuses = [self.Status.PENDING, self.Status.AWAITING_CONFIRMATION]
        return self.status in active_statuses and timezone.now() > self.expires_at

    def mark_expired_if_needed(self):
        if self.is_expired:
            self.status = self.Status.EXPIRED
            self.save(update_fields=['status', 'updated_at'])
        return self.status

    def __str__(self):
        return f"{self.tx_ref} — {self.application.full_name} — {self.status}"