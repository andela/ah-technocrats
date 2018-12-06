from authors.apps.profiles.models import Profile
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import User

@receiver(post_save, sender=User)
def create_new_profile(sender, instance, created, *args, **kwargs):
    """create the related profile for the registered user"""

    if instance and created: # create profile for new users only.
        instance.profile = Profile.objects.create(user=instance)
