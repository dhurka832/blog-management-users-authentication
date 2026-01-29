from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages


def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request,"Username already exists")
            return redirect('register')
        
        user = User.objects.create_user(username=username,password=password)
        user.save()
        messages.success(request,"Register Successful")
        return redirect('login')
    return render(request,"users/register.html")

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,"Login successfully")
            return redirect('all-posts')
        else:
            messages.error(request,"Invalid password or username")
    return render(request,"users/login.html")

def logout_user(request):
    logout(request)
    messages.success(request,"Logout successfully")
    return redirect('all-posts')

