from django.contrib import admin
from .models import PromoCode, Payment


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'school', 'discount_percent', 'is_active', 'valid_until', 'created_at')
    list_filter = ('school', 'is_active')
    search_fields = ('code',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('tx_ref', 'school', 'application', 'amount', 'status', 'reviewed_by', 'created_at')
    list_filter = ('status', 'school')
    search_fields = ('tx_ref', 'application__full_name')
    readonly_fields = ('tx_ref', 'created_at', 'updated_at')