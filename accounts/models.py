from django.db import models
from django.conf import settings

# Create your models here.
class Profile(models.Model): # user_id와 1:1 관계
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    nickname = models.CharField(max_length=40, blank=True)