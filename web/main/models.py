from django.db import models

# Create your models here.

class Stock(models.Model):
    stockCode = models.CharField(max_length=100)
    stockName = models.CharField(max_length=100)