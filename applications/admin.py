from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'school', 'course', 'status', 'cohort', 'applied_at')
    list_filter = ('status', 'school', 'course')
    search_fields = ('full_name', 'email', 'phone')
    readonly_fields = ('applied_at',)