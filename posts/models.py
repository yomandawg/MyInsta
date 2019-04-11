from django.db import models
# from django.contrib.auth.models import User # 직접 접근
from django.conf import settings

# Create your models here.
class Post(models.Model):
    content = models.CharField(max_length=150)
    image = models.ImageField(blank=True)
    # user = models.ForeignKey(User, on_delete=models.CASCADE) #User 폼 변경하려면 상속받아서 다르게 짜야함
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.content