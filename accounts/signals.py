from .models import User, Profile

from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def user_save_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
