from django.shortcuts import render,redirect
from .models import Post, Comment,Like, Profile
from .forms import RegistrationForm, LoginForm, PostForm, CommentForm, ProfilePictureForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse
# pagination
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
@login_required(login_url="/login/")
def index(request):
    
    user = request.user
    profile = Profile.objects.get(user=user)

    posts = Post.objects.filter(Q(creator__in=profile.following.all().values('user')) | Q(creator=user)).order_by('-creation_date')
    likes = Like.objects.all()
    comments = Comment.objects.all()
    
    form = PostForm()
    user_liked_posts = Like.objects.filter(like_owner=user, post__in=posts).values_list('post__id', flat=True)

    p = Paginator(posts,10)
    page = request.GET.get('page')
    posts_paginate = p.get_page(page)

    return render(request,'main/index.html',{'comments':comments,'posts':posts,'posts_paginate':posts_paginate,'likes':likes,'form':form,'profile':profile,'user_liked_posts':user_liked_posts})

@login_required(login_url="/login/")
def profile(request,pk):
    profile_user = User.objects.get(id=pk)
    user = request.user
    profile = Profile.objects.get(user=profile_user)

    form = PostForm()

    request_profile_friends = user.profile.following.all().values_list('id', flat=True)
    
    
    posts = Post.objects.filter(creator=profile_user).order_by('-creation_date')
    current_user_liked_posts = Like.objects.filter(like_owner=user, post__in=posts).values_list('post__id', flat=True)

    p = Paginator(posts,10)
    page = request.GET.get('page')
    posts_paginate = p.get_page(page)
    return render(request, 'others/profile.html', {'profile_friends':request_profile_friends,'form':form,'profile_user':profile_user,'user_liked_posts':current_user_liked_posts,'posts_paginate':posts_paginate,'profile':profile,"posts":posts,'user':user})


def user_login(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                
                login(request,user)
                return redirect('/')
            else:
                message = 'BAD DATA'
                return render(request,'registration/login.html',{'form':form,'message':message})
    else:
        
        form = LoginForm()
        return render(request,'registration/login.html',{'form':form})

def register(request):
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid:
            user = form.save()
            Profile.objects.create(user=user)
        return redirect('/login/')
    else:
        form = RegistrationForm()
        return render(request,'registration/register.html',{'form':form})
    
@login_required(login_url="/login/")
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST,request.FILES)
        current_url = request.POST['current_url']
        print(current_url)
        if form.is_valid:
            post = form.save(commit=False)
            post.creator = request.user
            post.save()
    else:
        form = PostForm()
        return render(request,'others/create_post.html',{'form':form})
    return redirect(f'{current_url}')

@login_required(login_url="/login/")
def post(request,pk):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.creator = request.user
            comment.post = Post.objects.get(id=pk)
            comment.save()
            amount_of_comments = Comment.objects.filter(post = comment.post).count()
            Post.objects.filter(id=comment.post.id).update(amount_of_comments=amount_of_comments)
        return redirect(f'/post/{pk}')
    else:
        post = Post.objects.get(id=pk)
        comments = Comment.objects.filter(post=post)
        user = request.user
        logged_in_user_profile = Profile.objects.get(user=user)
        post_creator = post.creator
        post_creator_profile = Profile.objects.get(user=post_creator)
        current_user_liked_posts = Like.objects.filter(like_owner=user, post=post).values_list('post__id', flat=True)
        form = CommentForm()

        delivery = {
            'user_liked_posts':current_user_liked_posts,
            'form':form,
            'post': post,
            'comments': comments,
            'user':user,
            'profile':logged_in_user_profile,
            'post_creator':post_creator,
            'post_creator_profile':post_creator_profile
        }

        return render(request,'others/post.html',delivery)
    
@login_required(login_url="/login/")
def like_post(request,pk):
    if request.method == "POST":
        user = request.user
        post_id = request.POST['post_id']
        post = Post.objects.filter(id=post_id).first()
        current_url = request.POST['current_url']
        
        if not Like.objects.filter(like_owner=user,post=post).exists():  
            Like.objects.create(like_owner=user,post=post)
        else:
            Like.objects.filter(like_owner=user,post=post).delete()

        amount_of_likes = Like.objects.filter(post = post).count()
        Post.objects.filter(id=post.id).update(amount_of_likes=amount_of_likes)

    return redirect(f'/{current_url}')
    
    

@login_required(login_url="/login/")
def edit_post(request,pk):
    post = Post.objects.get(id=pk)
    if post.creator == request.user:
        if request.method == 'POST':
            post_url = request.POST['post_url']
            form = PostForm(request.POST,request.FILES,instance=post)
            if form.is_valid():
                form.save()
            return redirect(f'{post_url}')
            
        else:
            form = PostForm(instance=post)
            return render(request,'others/edit_post.html',{'form':form,'post':post})

    else:
        return redirect('/')
    
@login_required(login_url="/login/")
def delete_post(request,pk):
    post = Post.objects.get(id=pk)
    if post.creator == request.user:
        Post.objects.filter(id=pk).delete()
    return redirect('/')

@login_required(login_url="/login/")
def profile_picture_change(request,pk):
    if request.method == "POST":
        profile = Profile.objects.get(id=pk)
        if profile.user == request.user:
            form = ProfilePictureForm(request.POST,request.FILES,instance=profile)

            if form.is_valid():
                profile = form.save(commit=False)
                profile.save()

        return redirect(f'/profile/{request.user.id}')
    
    else:
        form = ProfilePictureForm()
    return render(request, 'others/profile_picture_change.html',{'form':form,'profile_id':pk})

@login_required(login_url="/login/")
def search(request):
    if request.method == "POST":
        user_query = request.POST['user_query']
        users = User.objects.filter(Q(first_name__contains=user_query) | Q(last_name__contains=user_query)).all()
        return render(request,'others/search.html',{'searched_users':users,"query":user_query})
    else:
        return redirect('/')
    
@login_required(login_url="/login/")
def follow(request,pk):
    user = request.user
    profile_to_follow = Profile.objects.get(id=pk)

    # if profile_to_follow not in friends of user
    if profile_to_follow not in user.profile.following.all():
        user.profile.following.add(profile_to_follow)
    else:
        user.profile.following.remove(profile_to_follow)

    

    return redirect(f'/profile/{profile_to_follow.user.id}')
    
