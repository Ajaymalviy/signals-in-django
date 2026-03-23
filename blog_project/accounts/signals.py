from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from notifications.models import Notification

# Signal 1: auto-create profile when user registers
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        print(f"Profile created for {instance.username}")

# Signal 2: m2m_changed — notify when someone follows you
@receiver(m2m_changed, sender=Profile.following.through)
def notify_on_follow(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for pk in pk_set:
            followed_profile = Profile.objects.get(pk=pk)
            Notification.objects.create(
                recipient=followed_profile.user,
                message=f"{instance.user.username} started following you!"
            )