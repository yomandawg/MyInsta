from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

class CustomUserChangeForm(UserChangeForm): # 그냥 UserChangeForm에서 모듈화로 customize
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name'] # 어느 필드만 보여주고 싶다 선택 가능