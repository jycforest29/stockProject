from django.db import models
from user.models import User

# Create your models here.

class Post(models.Model):
    content = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="postAuthor")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    likeUsers = models.ForeignKey(User, on_delete=models.CASCADE, related_name="postLikeUsers", null = True)