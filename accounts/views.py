from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login # django에서 가져와 씀
from django.contrib.auth import logout as auth_logout


def login(request):
    if request.method == "POST":
        # POST: 실제 로그인(세션에 유저 정보 추가)
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'posts:list')
            # (parameter GET에서 받았을 때 'next'가 있으면 '/posts/13/like/') or 'posts:list'
            # next= 정의되어 있으면, 해당하는 url로 리다이렉트
            # else: 'posts:list'
    else:
        # GET: 로그인 정보 입력
        form = AuthenticationForm()
        
    return render(request, 'accounts/login.html', {'form': form})
    
    
def logout(request):
    auth_logout(request)
    return redirect('posts:list')
    