from django.db import models
from user.models import User
from stock.models import Stock
from django.utils import timezone

# Create your models here.
strategyType = [
        ('매수', '매수'),
        ('중립', '중립'),
        ('매도', '매도'), 
    ]
    
class Post(models.Model):
    # non-nullable field인데 일단
    title = models.CharField(max_length=30, null = True, blank = True)
    content = models.TextField(max_length=330)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="postAuthor")
    # non-nullable field인데 일단 null = True로 선언
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name="postStock")    
    strategy = models.CharField(max_length=3, choices=strategyType, default = "중립")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(default = timezone.now)
    likeUsers = models.ManyToManyField(User, related_name="postLikeUsers")
    likeCount = models.PositiveIntegerField(default = 0)
    commentCount = models.PositiveIntegerField(default = 0) 