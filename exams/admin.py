from django.contrib import admin
from .models import Exam


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'cohort', 'total_marks', 'exam_date', 'created_by')
    list_filter = ('school', 'cohort')
    search_fields = ('title', 'description')