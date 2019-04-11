from django.shortcuts import render, redirect
from .forms import PostForm
from .models import Post
from django.views.decorators.http import require_POST

# Create your views here.
def create(request):
    if request.method == "POST":
        # 작성된 post를 DB에 적용
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:list')
    else: # GET
        # post를 작성하는 form을 보여줌
        form = PostForm()
        return render(request, 'posts/create.html', {'form': form})

def list(request):
    posts = Post.objects.all()
    return render(request, 'posts/list.html', {'posts': posts})
    
def read(request, post_id):
    post = Post.objects.get(id=post_id)
    return render(request, 'posts/read.html', {'post': post})

def update(request, post_id):
    p = Post.objects.get(id=post_id)
    if request.method == "POST":
        # 작성된 post를 DB에 적용
        form = PostForm(request.POST, instance=p)
        if form.is_valid():
            form.save()
            return redirect('posts:list')
    else: # GET
        # post를 작성하는 form을 보여줌
        form = PostForm(instance=p)
        return render(request, 'posts/create.html', {'form': form})

# @require_POST
def delete(request, post_id):
    p = Post.objects.get(id=post_id)
    p.delete()
    return redirect('posts:list')