from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import Profile

class CustomUserChangeForm(UserChangeForm): # 그냥 UserChangeForm에서 모듈화로 customize
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name'] # 어느 필드만 보여주고 싶다 선택 가능

# 기존의 UserCreationForm을 override
class CustomUserCreationForm(UserCreationForm): # custom User model을 위한 creation form
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        # fields = UserCreationForm.Meta.fields # 원래 있던 fields 그대로 써
        
class ProfileForm(forms.ModelForm): # user profile 수정하기 위해
    class Meta:
        model = Profile
        fields = ['description', 'nickname', 'image']