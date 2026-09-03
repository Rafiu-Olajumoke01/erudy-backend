from django.contrib import admin
from .models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('application', 'exam', 'score', 'graded_by', 'graded_at')
    list_filter = ('exam',)
    search_fields = ('application__full_name',)