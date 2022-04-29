from django.db import models
from user.models import User
from post.models import Post

# Create your models here.

class Comment(models.Model):
    # post모델과 구별되는 comment모델의 필드인 post를 제외하고 나머지 필드는 post 모델과 같은 필드명으로 함
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="commentPost")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentAuthor")
    content = models.CharField(max_length=300)    
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    likeUsers = models.ManyToManyField(User, related_name="commentLikeUsers")
    likeCount = models.PositiveIntegerField(default = 0)
