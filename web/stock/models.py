from django.db import models

# Create your models here.

from user.models import User

class Stock(models.Model):
    stockCode = models.CharField(max_length=6)
    stockName = models.CharField(max_length=100)
    ipoDate = models.DateField()
    kospi = models.CharField(max_length=6)
    perValue = models.CharField(max_length=11)
    stockNum = models.PositiveBigIntegerField()
    likeUsers = models.ManyToManyField(User, related_name='stockLikeUsers')
    likeCount = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return self.stockName