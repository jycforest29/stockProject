from django.db import models

# Create your models here.

from user.models import User

class Stock(models.Model):
    stockCode = models.CharField(max_length=6)
    stockName = models.CharField(max_length=100)
    ipoDate = models.CharField(max_length=11)
    kospi = models.CharField(max_length=6)
    perValue = models.PositiveIntegerField(default = 0)
    stockNum = models.PositiveBigIntegerField()
    # likeUsers = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stockLikeUsers', null = True)