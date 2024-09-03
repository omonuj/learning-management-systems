from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User, UserProfile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, full_name=instance.full_name)


def save_user_profile(sender, instance, **kwargs):
    instance.user_profile.save()