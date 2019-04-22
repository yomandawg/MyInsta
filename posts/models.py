from django.db import models
# from django.contrib.auth.models import User # 직접 접근
from django.conf import settings
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFit

# Create your models here.
class Post(models.Model):
    content = models.CharField(max_length=150)
    # image = models.ImageField(blank=True)
    
    # resized image
    image = ProcessedImageField(processors=[ResizeToFit(width=960, upscale=False)], format='JPEG')
    image_thumbnail = ImageSpecField(source='image', processors=[ResizeToFit(width=320, upscale=False)], format='JPEG', options={'quality': 60})
    # date option
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # user = models.ForeignKey(User, on_delete=models.CASCADE) #User 폼 변경하려면 상속받아서 다르게 짜야함
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # user foreign_key를 불러오므로 user_id 키가 있을 것
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_posts", blank=True) # user와 M:M 관계
    # M:M은 쌍방향이라 어느쪽에 테이블을 만들어도 상관 없음; users에 넣어도 됨(초기 설계단계에서 설정) # related_name에 양쪽 다 조회할 수 있게끔 이름 설정
    # users like 가 문법적으로 맞지만 users model을 접근하기가 일단 어렵기 때문에 이렇게 함
    
    def __str__(self):
        return self.content
        
        
class Comment(models.Model):
    content = models.CharField(max_length=100)
    # 두 개의 Foreign key를 갖게됨
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # 어떤 모델을 참조하고 있는지
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.content
        
        
# ADD HASHTAG 기능
# class Post(models.Model):
#     title = models.CharField(max_length=100)
#     content = models.CharField(max_length=300)
#     hashtag = models.ManyToManyField(Hashtag)
    
# class Hashtag(models.Model):
#     content = models.CharField(max_length=50)