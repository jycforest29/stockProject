from django.db import models
from user.models import User

# Create your models here.

class Stock(models.Model):
    stockCode = models.CharField(max_length=30)
    stockName = models.CharField(max_length=30)
    # 시가총액(억)
    value = models.PositiveIntegerField()
    # 자산총계(억)
    totalAssets = models.DecimalField(max_digits=9,decimal_places=2)
    per = models.DecimalField(max_digits=6, decimal_places=2)
    roa = models.DecimalField(max_digits=6,decimal_places=2)
    roe = models.DecimalField(max_digits=6,decimal_places=2)
    # 매출액(억)
    take = models.PositiveIntegerField()
    # 매출액증가율
    takeRatio = models.DecimalField(max_digits=9,decimal_places=2)
    # 액면가
    perValue = models.PositiveIntegerField()
    # 영업이익(백만)
    operatingProfit = models.PositiveIntegerField()
    ipoDate = models.DateField()
    # likeUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stockLikeUser")
    # buyUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stockBuyUser")