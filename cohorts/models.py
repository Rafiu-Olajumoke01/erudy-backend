from django.conf import settings
from django.db import models
from tenants.models import School


class Course(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='courses',
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    duration_weeks = models.PositiveIntegerField(help_text="Duration of the course in weeks")
    fee = models.DecimalField(max_digits=12, decimal_places=2, help_text="Course fee in Naira")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('school', 'name')

    def __str__(self):
        return f"{self.name} ({self.school.name})"


class Cohort(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('current', 'Current'),
        ('completed', 'Completed'),
    ]

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='cohorts',
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='cohorts',
    )
    name = models.CharField(max_length=150, help_text="e.g. 'July 2026 Batch'")
    tutor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cohorts_taught',
        limit_choices_to={'role': 'tutor'},
    )
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('school', 'name')
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.name} ({self.school.name})"

    @property
    def student_count(self):
        # Counts applications assigned to this cohort.
        # Will connect once the `applications` app exists with a FK to Cohort.
        return self.applications.count()