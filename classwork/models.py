from django.conf import settings
from django.db import models
from tenants.models import School
from cohorts.models import Cohort
from academics.models import ClassSession


class Classwork(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='classworks',
    )
    cohort = models.ForeignKey(
        Cohort,
        on_delete=models.CASCADE,
        related_name='classworks',
    )
    session = models.ForeignKey(
        ClassSession,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='classworks',
        help_text="Optional — link to the specific session this classwork was given in",
    )
    title = models.CharField(max_length=255)
    instructions = models.TextField(blank=True)
    attachment = models.FileField(upload_to='classwork/', blank=True, null=True)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='classwork_posted',
        limit_choices_to={'role': 'tutor'},
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.cohort.name})"


class ClassworkSubmission(models.Model):
    classwork = models.ForeignKey(
        Classwork,
        on_delete=models.CASCADE,
        related_name='submissions',
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='classwork_submissions',
        limit_choices_to={'role': 'student'},
    )
    content = models.TextField(blank=True)
    attachment = models.FileField(upload_to='classwork_submissions/', blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('classwork', 'student')
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student.username} — {self.classwork.title}"