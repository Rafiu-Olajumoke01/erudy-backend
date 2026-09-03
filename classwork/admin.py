from django.contrib import admin
from .models import Classwork, ClassworkSubmission


@admin.register(Classwork)
class ClassworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'cohort', 'session', 'posted_by', 'created_at')
    list_filter = ('school', 'cohort')
    search_fields = ('title', 'instructions')


@admin.register(ClassworkSubmission)
class ClassworkSubmissionAdmin(admin.ModelAdmin):
    list_display = ('classwork', 'student', 'submitted_at')
    list_filter = ('classwork',)
    search_fields = ('student__username',)