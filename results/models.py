from django.conf import settings
from django.db import models
from exams.models import Exam
from applications.models import Application


class Result(models.Model):
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        related_name='results',
    )
    application = models.ForeignKey(
        Application,
        on_delete=models.CASCADE,
        related_name='results',
    )
    score = models.DecimalField(max_digits=6, decimal_places=2)
    remarks = models.TextField(blank=True)
    graded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='results_graded',
    )
    graded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('exam', 'application')
        ordering = ['-graded_at']

    def __str__(self):
        return f"{self.application.full_name} — {self.exam.title}: {self.score}"

    @property
    def percentage(self):
        if self.exam.total_marks:
            return round((float(self.score) / self.exam.total_marks) * 100, 1)
        return None