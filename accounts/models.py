from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Profile(models.Model): # user_id와 1:1 관계
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    nickname = models.CharField(max_length=40, blank=True)
    
class User(AbstractUser): # 앞으로 정의한 유저는 이것 -> settings.py에서 django에게 알려줘야해
    follows = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followings")