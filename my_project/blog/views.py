from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q 
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Post
from .forms import PostForm

def home(request):
    query = request.GET.get('q')
    posts = Post.objects.select_related('author')
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query))
    posts = posts.order_by('created_at')
    paginator = Paginator(posts,5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request,"home.html",{'posts':posts})

def detail_post(request,pk):
    post = Post.objects.get(id=pk)
    return render(request,"post_detail.html",{'post':post})

@login_required
def my_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request,"my_post.html",{'posts':posts})

@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user 
            post.save()
            messages.success(request,"Post created successfully")
            return redirect('my-posts')
    else:
        form = PostForm()
    return render(request,"create_post.html",{'form':form})

@login_required
def update_post(request,pk):
    post = Post.objects.get(id=pk,author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,"Post updated successfully")
            return redirect('my-posts')
    else:
        form = PostForm(instance=post)
    return render(request,"update_post.html",{'form':form})

@login_required
def delete_post(request,pk):
    post = Post.objects.get(id=pk,author=request.user)
    post.delete()
    messages.success(request,"Post deleted successfully")
    return redirect('my-posts')

def register_view(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request,user)
        messages.success(request,"Register successfully")
        return redirect('my-posts')
    return render(request,"register.html",{'form':form})

def login_view(request):
    form = AuthenticationForm(request,data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request,user)
        messages.success(request,"Login successfully")
        return redirect('my-posts')
    return render(request,"login.html",{'form':form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request,"Logout successfully")
    return redirect('all-posts')

