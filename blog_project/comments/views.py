from django.shortcuts import get_object_or_404
from .models import Comment
from posts.models import Post
from .signals import comment_posted

def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = Comment.objects.create(
        post=post,
        author=request.user,
        body=request.POST.get('body')
    )
    # manually fire custom signal
    comment_posted.send(sender=Comment, comment=comment)
    ...