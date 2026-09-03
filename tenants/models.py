from django.db import models
from django.utils.text import slugify


class School(models.Model):
    SUBSCRIPTION_PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('pro', 'Pro'),
        ('enterprise', 'Enterprise'),
    ]

    SUBSCRIPTION_STATUS_CHOICES = [
        ('trial', 'Trial'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('suspended', 'Suspended'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)

    subscription_plan = models.CharField(
        max_length=20,
        choices=SUBSCRIPTION_PLAN_CHOICES,
        default='basic',
    )
    subscription_status = models.CharField(
        max_length=20,
        choices=SUBSCRIPTION_STATUS_CHOICES,
        default='trial',
    )

    is_active = models.BooleanField(default=True)
    date_onboarded = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name