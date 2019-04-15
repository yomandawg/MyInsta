from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login # django에서 가져와 씀
from django.contrib.auth import logout as auth_logout


def login(request):
    username = request.POST('username')
    password = request.POST('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        auth_login(request, user)
        redirect('posts:list')
    else:
        render(request, 'accounts/login.html')

def logout(request):
    auth_logout(request)
    redirect('posts:list')