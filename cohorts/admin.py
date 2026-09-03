from django.contrib import admin

from .models import Course, Cohort


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'school', 'duration_weeks', 'is_active', 'created_at']
    list_filter = ['school', 'is_active']
    search_fields = ['name']


@admin.register(Cohort)
class CohortAdmin(admin.ModelAdmin):
    list_display = ['name', 'school', 'course', 'tutor', 'status', 'start_date', 'end_date', 'is_active']
    list_filter = ['school', 'status', 'is_active']
    search_fields = ['name']