from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
from .models import Post
from django.views.decorators.http import require_POST

# Create your views here.
def list(request):
    posts = Post.objects.all()
    return render(request, 'posts/list.html', {'posts': posts})

def create(request):
    if request.method == "POST":
        # 작성된 post를 DB에 적용
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
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