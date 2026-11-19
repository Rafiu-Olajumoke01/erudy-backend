from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from tenants.models import School


class ParentStudentLink(models.Model):
    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='children_links',
        limit_choices_to={'role': 'parent'},
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='parent_links',
        limit_choices_to={'role': 'student'},
    )
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='parent_links',
    )
    relationship = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('parent', 'student')

    def clean(self):
        if self.parent.role != 'parent':
            raise ValidationError("The parent user must have the Parent role.")
        if self.student.role != 'student':
            raise ValidationError("The student user must have the Student role.")
        if self.parent.school_id != self.school_id or self.student.school_id != self.school_id:
            raise ValidationError("Parent and student must belong to this school.")

    def __str__(self):
        return f"{self.parent.username} -> {self.student.username}"