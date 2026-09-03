from django.contrib.auth.models import AbstractUser
from django.db import models
from tenants.models import School


class User(AbstractUser):
    class Role(models.TextChoices):
        PLATFORM_OWNER = 'platform_owner', 'Platform Owner'
        SCHOOL_ADMIN = 'school_admin', 'School Admin'
        TUTOR = 'tutor', 'Tutor'
        STUDENT = 'student', 'Student'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
    )

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='users',
        null=True,
        blank=True,
        help_text="Leave blank for Platform Owner — they aren't tied to a single school."
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"