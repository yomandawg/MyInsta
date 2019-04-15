from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
# login_required
# 1. 유저가 로그인 안했으면, 로그인창으로 보냄 - default = accounts
# 2. "https://sitback-sitback.c9users.io/accounts/login/?next=/posts/1/like"
# next:로그인 되는 순간 like 하게 만들겠다. url 끝난다음에 어디로 가는지 고려


# Create your views here.
def list(request):
    posts = Post.objects.all()
    return render(request, 'posts/list.html', {'posts': posts})

def create(request):
    if request.method == "POST":
        # 작성된 post를 DB에 적용
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:list')
    else: # GET
        # post를 작성하는 form을 보여줌
        form = PostForm()
        return render(request, 'posts/create.html', {'form': form})
    
def read(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'posts/read.html', {'post': post})

def update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.user != request.user:
        return redirect('post:list')
    if request.method == "POST":
        # 실제 DB에 수정 반영
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:list')
    else:
        form = PostForm(instance=post)
        return render(request, 'posts/update.html', {'form': form})
    
    # p = Post.objects.get(id=post_id)
    # if request.method == "POST":
    #     # 작성된 post를 DB에 적용
    #     form = PostForm(request.POST, instance=p)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('posts:list')
    # else: # GET
    #     # post를 작성하는 form을 보여줌
    #     form = PostForm(instance=p)
    #     return render(request, 'posts/create.html', {'form': form})

# @require_POST
def delete(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if post.user != request.user:
        return redirect('posts:list')
    post.delete()
    return redirect('posts:list')
    
    
@login_required # session에 로그인이 안돼있으면 막음
def like(request, post_id):
    # 1. like를 추가할 포스트를 가져옴
    post = get_object_or_404(Post, id=post_id)
    # post = Post.objects.get(id=post_id)
    
    # 2. 만약 유저가 해당 post를 이미 like 했다면,
    #       like를 제거하고,
    #    아니면,
    #       like를 추가한다.
    if request.user in post.like_users.all(): # 유저가 post.like_users.all() -> queryset 리스트 안에 있으면,
        post.like_users.remove(request.user) # like 해제
    else:
        post.like_users.add(request.user)
        
    return redirect('posts:list')