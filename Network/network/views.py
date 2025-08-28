from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.forms import ModelForm
from django import forms
from django.core.paginator import Paginator
from django.views.generic import UpdateView
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse


from .models import User, Post


def index(request):


    posts = Post.objects.all().order_by("-timestamp") 

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html",{

        'page_obj': page_obj,
        
        # "posts": posts
       
    
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# new post
class NewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['Description']


@login_required 
def new_post(request):

    if request.method == "POST":
        form = NewPostForm(request.POST)

        if form.is_valid():
           Description =  form.cleaned_data["Description"]
           creator = request.user
           
           Post.objects.create(creator = creator, Description = Description)
        #    posts.append(creator)
        #    posts.append(post)
           return HttpResponseRedirect(reverse(index))
        else:
            return render(request, "network/new-post.html",{
                "form": NewPostForm()
            })
    else:
        
        return render(request, "network/new-post.html",{
        "form": NewPostForm()
    })



def P(request, creator):


    user = request.user

    profile = User.objects.get(username = creator)
    posts = Post.objects.filter(creator = profile).order_by('-timestamp')

    profile_followers = profile.followers.all()
    profile_following = profile.following.all()

    followers_count = len(profile_followers)
    following_count = len(profile_following)


    if user in profile_followers:
        already_followed = True
    else:
        already_followed = False



    if request.method == "POST":
        if request.POST.get("button") == "Unfollow":
            profile.followers.remove(user)
        elif request.POST.get("button") == "Follow":
            profile.followers.add(user)

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, "network/profile.html",{
         "posts": posts,
         "profile": profile,
         "followers": followers_count,
         "following": following_count,
         "already_followed": already_followed,
         'page_obj': page_obj,
     })

def following(request):


    viewer = User.objects.get(username = request.user)

    viewer_following_list = viewer.following.all()

    posts = Post.objects.filter(creator__in = viewer_following_list).order_by('-timestamp')

    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/following.html",{
        "posts":posts,
        'page_obj': page_obj,
    })

 


class EditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['Description']



@login_required
def edit(request, post_id):
    

    post = Post.objects.get(id = post_id)
    form = EditForm(instance = post)


    if request.method == "POST":
        form = EditForm(request.POST, instance = post)
        # form['post'].value()
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(index))

        else:
            return render(request, "network/edit.html",{
            "post":post,
            "form": form,

        })

    else:
        return render(request, "network/edit.html",{
            "post":post,
            "form": form,
        }

)



@login_required
def like(request, post_id):

    user = request.user

    post = Post.objects.get(id = post_id)


    post_likers = post.liked_by.all()

    if user in post_likers:
        change = False
        post.liked_by.remove(user)
    else:
        change = True
        post.liked_by.add(user)
    post.save()
    return JsonResponse({"liked": change, "likes_count": post.liked_by.count() }, status= 200)
