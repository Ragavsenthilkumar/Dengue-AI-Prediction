from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """Extra user info with role-based access."""
    ROLE_CHOICES = [
        ('citizen', 'Citizen'),
        ('officer', 'Government Officer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='citizen')
    phone = models.CharField(max_length=20, blank=True)
    area = models.CharField(max_length=100, blank=True, help_text='City / locality / ward')

    def __str__(self):
        return f'{self.user.username} ({self.get_role_display()})'

    @property
    def is_officer(self):
        return self.role == 'officer'

    @property
    def is_citizen(self):
        return self.role == 'citizen'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

