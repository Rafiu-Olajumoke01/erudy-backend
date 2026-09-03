from django.conf import settings
from django.db import models
from academics.models import ClassSession
from applications.models import Application


class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
    ]

    session = models.ForeignKey(
        ClassSession,
        on_delete=models.CASCADE,
        related_name='attendance_records',
    )
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='attendance_records',
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='attendance_marked',
    )
    marked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session', 'application')
        ordering = ['-marked_at']

    def __str__(self):
        return f"{self.application.full_name} — {self.session.date} — {self.status}"