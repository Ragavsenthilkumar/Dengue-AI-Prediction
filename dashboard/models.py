from django.db import models
from django.contrib.auth.models import User


class Report(models.Model):
    RISK_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    risk_level = models.CharField(max_length=10, choices=RISK_LEVELS, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    image = models.FileField(upload_to='reports/', blank=True, null=True)
    reported_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='reports', verbose_name='Reported by'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ActionAlert(models.Model):
    """Urgent instruction issued by an officer for immediate action."""
    PRIORITY_CHOICES = [
        ('urgent', 'Urgent'),
        ('normal', 'Normal'),
    ]

    title = models.CharField(max_length=200)
    message = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    issued_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='action_alerts',
        verbose_name='Issued by officer'
    )
    report = models.ForeignKey(
        Report, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='alerts'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

