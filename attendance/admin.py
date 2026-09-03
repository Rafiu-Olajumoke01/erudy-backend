from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('application', 'session', 'status', 'marked_by', 'marked_at')
    list_filter = ('status', 'session')
    search_fields = ('application__full_name',)