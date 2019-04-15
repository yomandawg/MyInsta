from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login as auth_login # django에서 가져와 씀
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model


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
    
def signup(request):
    if request.method == "POST":
        # POST: 유저 등록
        form = UserCreationForm(request.POST) # UserCreationForm이 알아서 column에 넣어주고
        if form.is_valid():
            user = form.save()
            # auth_login(request, form.get_user()) 로그인과 달리 form 형식 달라서 이거 안됨
            auth_login(request, user) # signup 후 바로 로그인
            return redirect('posts:list')
    else:
        # GET: 유저 정보 입력
        form = UserCreationForm()
        
    return render(request, 'accounts/signup.html', {'form': form})
    

def people(request, username):
    # 사용자에 대한 정보
    people = get_object_or_404(get_user_model(), username=username) # 모델과 keyword 인자로 가능
    # 1. settings.AUTH_USER_MODEL - 이건 views를 쓰기 힘듦
    # 2. get_user_model() 실제 user클래스를 바로 리턴시켜줌 - 되도록이면 이거 쓰자
    # 3. User (django.contrib.auth.models에 들어가있는) 그냥 가져오기 - 안쓰는게 좋아
    return render(request, 'accounts/people.html', {'people': people})