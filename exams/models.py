from django.conf import settings
from django.db import models
from tenants.models import School
from cohorts.models import Cohort


class Exam(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='exams',
    )
    cohort = models.ForeignKey(
        Cohort,
        on_delete=models.CASCADE,
        related_name='exams',
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    total_marks = models.PositiveIntegerField(default=100)
    exam_date = models.DateField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='exams_created',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.cohort.name})"