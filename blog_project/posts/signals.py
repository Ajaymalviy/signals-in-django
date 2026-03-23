from django.db.models.signals import pre_save, post_save, pre_delete, post_migrate
from django.dispatch import receiver
from django.utils.text import slugify
from notifications.models import Notification
from .models import Post, Category

# Signal 3: pre_save — auto-generate slug before saving
@receiver(pre_save, sender=Post)
def auto_slug(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)

# Signal 4: post_save — notify followers when post is published
@receiver(post_save, sender=Post)
def notify_followers_on_publish(sender, instance, created, **kwargs):
    if instance.is_published:
        followers = instance.author.profile.followers.all()
        for follower_profile in followers:
            Notification.objects.create(
                recipient=follower_profile.user,
                message=f"{instance.author.username} published: {instance.title}"
            )

# Signal 5: pre_delete — log before a post is deleted
@receiver(pre_delete, sender=Post)
def log_post_deletion(sender, instance, **kwargs):
    print(f"[LOG] Post '{instance.title}' by {instance.author} is being deleted.")

# Signal 6: post_migrate — seed default categories
@receiver(post_migrate)
def create_default_categories(sender, **kwargs):
    if sender.name == 'posts':
        for name in ['Technology', 'Lifestyle', 'News']:
            Category.objects.get_or_create(name=name)