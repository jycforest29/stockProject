from django.db import models
from user.models import User
from post.models import Post

# Create your models here.

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="commentPost")
    content = models.CharField(max_length=300)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentCommenter")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    likeUsers = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentLikeUsers", null = True)
