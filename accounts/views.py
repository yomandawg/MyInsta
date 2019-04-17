from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import login as auth_login # django에서 가져와 씀
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model, update_session_auth_hash
from .forms import CustomUserChangeForm, ProfileForm
from .models import Profile


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
            Profile.objects.create(user=user) # 1:1 profile도 함께 만들어줌
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
    
    
# 회원 정보 변경(편집 & 반영)
def update(request):
    if request.method == "POST":
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_change_form.is_valid() and profile_form.is_valid():
            user = user_change_form.save() # save된 객체를 return함
            profile_form.save()
            return redirect('people', user.username)
    else: # GET: 지금 로그인한 유저의 현재 정보를 띄워주는 form
        user_change_form = CustomUserChangeForm(instance=request.user)
        
        # instance에넣어줄 정보가 있는 User가 있고, 없는 User도 있다.
        # if Profile.objects.get(user=request): # 프로필이 있냐 없냐
        #     profile = Profile.objects.get(user=request) # 있으면 가져와
        # else:
        #     profile = Profile.objects.create(user=request.user) # 유저의 정보가 들어있는 비어있는 profile
        profile, created = Profile.objects.get_or_create(user=request.user) # return이 tuple형 (get성공, created)
        profile_form = ProfileForm(instance=profile) # profile도 같이 수정해주기
        
        # 현재 로그인된 정보 but 이것만 출력하면 너무 많아 -> 원하는 정보만 보게 수정해야함
        # password_change_form = PasswordChangeForm(request.user)
        # context = {'user_change_form': user_change_form, 'password_change_form': password_change_form} # 서로 다른 페이지로 만들거다
        context = {
            'user_change_form': user_change_form,
            'profile_form': profile_form,
        }
        return render(request, 'accounts/update.html', context)
        
        
# 회원 탈퇴
def delete(request):
    if request.method == "POST":
        request.user.delete()
        return redirect('posts:list')
    return render(request, 'accounts/delete.html')


# 비밀번호 변경
def password(request):
    if request.method == "POST":
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save() # 그냥 이렇게 하면 session 로그아웃됨 -> login상태 유지하려면?
            update_session_auth_hash(request, user) # auth hash 자동 업데이트 - 로그인 유지
            return redirect('people', user.username)
    else:
        password_change_form = PasswordChangeForm(request.user)
        return render(request, 'accounts/password.html', {'password_change_form': password_change_form})