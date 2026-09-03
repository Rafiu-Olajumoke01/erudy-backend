from django.conf import settings
from django.db import models
from tenants.models import School


class Announcement(models.Model):
    AUDIENCE_CHOICES = [
        ('all', 'Everyone'),
        ('students', 'Students Only'),
        ('tutors', 'Tutors Only'),
    ]

    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='announcements',
    )
    title = models.CharField(max_length=255)
    content = models.TextField()
    audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES, default='all')
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='announcements_posted',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Message(models.Model):
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages_sent',
    )
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='messages_received',
    )
    subject = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
    )
    is_warning = models.BooleanField(default=False, help_text="Flag this message as a formal warning/query")
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender} → {self.recipient}: {self.subject or self.content[:30]}"