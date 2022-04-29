from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.

class User(AbstractUser):
    strategyType = [
        ('안전형', '안전형'),
        ('중립형', '중립형'),
        ('위험형', '위험형'),
    ]
    # 오버라이드
    email = models.EmailField(unique = True)
    strategy = models.CharField(max_length=3, choices=strategyType, default = "안전형")
    
