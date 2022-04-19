from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.

class User(AbstractUser):
    profit = models.PositiveIntegerField(default=0)
    profitPerKospi = models.PositiveIntegerField(default=0)
    profitPerSector1 = models.PositiveIntegerField(default=0)
    profitPerSector2 = models.PositiveIntegerField(default=0)
    profitPerSector3 = models.PositiveIntegerField(default=0)
    profitPerLikes = models.PositiveIntegerField(default=0)
