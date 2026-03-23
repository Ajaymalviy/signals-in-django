from django.dispatch import Signal, receiver
from notifications.models import Notification

comment_posted = Signal()

# Signal 7: custom signal — notify post author on new comment
@receiver(comment_posted)
def notify_author_on_comment(sender, comment, **kwargs):
    Notification.objects.create(
        recipient=comment.post.author,
        message=f"{comment.author.username} commented on your post '{comment.post.title}'"
    )