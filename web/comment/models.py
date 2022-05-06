from django.db import models
from user.models import User
from post.models import Post
from django.utils import timezone

# Create your models here.

class Comment(models.Model):
    # post모델과 구별되는 comment모델의 필드인 post를 제외하고 나머지 필드는 post 모델과 같은 필드명으로 함
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="commentPost")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentAuthor")
    content = models.CharField(max_length=50)    
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(default = timezone.now)
    likeUsers = models.ManyToManyField(User, related_name="commentLikeUsers")
    likeCount = models.PositiveIntegerField(default = 0)
 
class ReComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="reCommentComment")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reCommentAuthor")
    content = models.CharField(max_length=50)    
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(default = timezone.now)
    likeUsers = models.ManyToManyField(User, related_name="reCommentLikeUsers")
    likeCount = models.PositiveIntegerField(default = 0)