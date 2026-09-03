from django.conf import settings
from django.db import models
from tenants.models import School
from cohorts.models import Course, Cohort


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='applications',
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='applications',
    )

    # Applicant info — captured directly since they don't have a User account yet
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    # Linked once the applicant is approved, pays, and gets a real account
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications',
        limit_choices_to={'role': 'student'},
    )

    # Set once the School Admin assigns them to an actual cohort
    cohort = models.ForeignKey(
        Cohort,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='applications',
    )

    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.full_name} — {self.course.name} ({self.status})"