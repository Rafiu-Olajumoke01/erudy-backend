from django.db import models
from django.conf import settings
from tenants.models import School


class Certificate(models.Model):
    """One certificate per student. Re-uploading replaces the existing file."""
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='certificates',
    )
    student = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='certificate',
        limit_choices_to={'role': 'student'},
    )
    file = models.FileField(upload_to='certificates/')
    issued_date = models.DateField(null=True, blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='certificates_uploaded',
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Certificate for {self.student}"