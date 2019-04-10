from django.shortcuts import render, redirect
from .forms import PostForm

# Create your views here.
def create(request):
    if request.method == "POST":
        # 작성된 post를 DB에 적용
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:create')
    else: # GET
        # post를 작성하는 form을 보여줌
        form = PostForm()
        return render(request, 'posts/create.html', {'form': form})

def list(request):
    posts = Post.objects.all()
    
    return render(request, 'posts/list.html', {'posts': posts})
    