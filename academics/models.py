from django.conf import settings
from django.db import models
from tenants.models import School
from cohorts.models import Cohort


class ClassSession(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='class_sessions',
    )
    cohort = models.ForeignKey(
        Cohort,
        on_delete=models.CASCADE,
        related_name='class_sessions',
    )
    tutor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='class_sessions_taught',
        limit_choices_to={'role': 'tutor'},
    )
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    topics_covered = models.TextField(
        blank=True,
        help_text="Topics covered in this session — one per line, or comma-separated"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-start_time']

    def __str__(self):
        return f"{self.cohort.name} — {self.date}"

    @property
    def duration_hours(self):
        from datetime import datetime
        start = datetime.combine(self.date, self.start_time)
        end = datetime.combine(self.date, self.end_time)
        return round((end - start).seconds / 3600, 2)


class ClassNote(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='class_notes',
    )
    session = models.ForeignKey(
        ClassSession,
        on_delete=models.CASCADE,
        related_name='notes',
    )
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    attachment = models.FileField(upload_to='class_notes/', blank=True, null=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='notes_uploaded',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.session})"


class Assignment(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='assignments',
    )
    cohort = models.ForeignKey(
        Cohort,
        on_delete=models.CASCADE,
        related_name='assignments',
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    attachment = models.FileField(upload_to='assignments/', blank=True, null=True)
    due_date = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='assignments_created',
        limit_choices_to={'role': 'tutor'},
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.cohort.name})"


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions',
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assignment_submissions',
        limit_choices_to={'role': 'student'},
    )
    content = models.TextField(blank=True)
    attachment = models.FileField(upload_to='assignment_submissions/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('assignment', 'student')
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student.username} — {self.assignment.title}"


class CapstoneGuideline(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='capstone_guidelines',
    )
    cohort = models.ForeignKey(
        Cohort,
        on_delete=models.CASCADE,
        related_name='capstone_guidelines',
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    attachment = models.FileField(upload_to='capstone_guidelines/', blank=True, null=True)
    deadline = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='capstone_guidelines_created',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.cohort.name})"