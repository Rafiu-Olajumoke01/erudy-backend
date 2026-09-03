from django.contrib import admin
from .models import School


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'subscription_plan', 'subscription_status', 'is_active', 'date_onboarded')
    list_filter = ('subscription_plan', 'subscription_status', 'is_active')
    search_fields = ('name', 'email', 'slug')
    prepopulated_fields = {'slug': ('name',)}