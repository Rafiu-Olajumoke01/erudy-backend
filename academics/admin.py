from django.contrib import admin
from .models import ClassSession, ClassNote, Assignment, AssignmentSubmission, CapstoneGuideline


@admin.register(ClassSession)
class ClassSessionAdmin(admin.ModelAdmin):
    list_display = ('cohort', 'tutor', 'date', 'start_time', 'end_time', 'school')
    list_filter = ('school', 'cohort')
    search_fields = ('cohort__name', 'topics_covered')


@admin.register(ClassNote)
class ClassNoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'session', 'uploaded_by', 'created_at')
    list_filter = ('school',)
    search_fields = ('title', 'content')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'cohort', 'due_date', 'created_by', 'created_at')
    list_filter = ('school', 'cohort')
    search_fields = ('title', 'description')


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at')
    list_filter = ('assignment',)
    search_fields = ('student__username',)


@admin.register(CapstoneGuideline)
class CapstoneGuidelineAdmin(admin.ModelAdmin):
    list_display = ('title', 'cohort', 'deadline', 'created_by', 'created_at')
    list_filter = ('school', 'cohort')
    search_fields = ('title', 'description')