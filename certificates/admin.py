from django.contrib import admin
from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('student', 'school', 'issued_date', 'uploaded_by', 'uploaded_at')
    list_filter = ('school',)
    search_fields = ('student__username', 'student__email')