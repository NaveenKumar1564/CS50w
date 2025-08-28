from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required
from django import forms
from django.http import JsonResponse

from .models import *


def index(request):
    
    all_songs = Songs.objects.all().order_by("Title")

    return render(request, "music/index.html",{

        'songs':all_songs

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
            return render(request, "music/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "music/login.html")


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
            return render(request, "music/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "music/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "music/register.html")


class NewAudioForm(ModelForm):
    class Meta:
        model = Songs
        fields = [ 'Title', 'Singer', 'Audio', 'Albums']


@login_required
def new_audio(request):
    if request.method== "POST":
        form = NewAudioForm(request.POST, request.FILES)
        if form.is_valid():
            Title =  form.cleaned_data['Title']
            Singer =  form.cleaned_data['Singer']
            Audio =  form.cleaned_data['Audio']
            Albums =  form.cleaned_data['Albums']
            Poster = request.user
            Songs.objects.create(Poster = Poster, Title = Title, Singer = Singer, Audio = Audio, Albums = Albums)
        
           
            return HttpResponseRedirect(reverse(index))
        else:
            return render(request, "music/new_audio.html",{
                'form': NewAudioForm()
            })
    else:
        return render(request, "music/new_audio.html",{
            "form": NewAudioForm()
            })
    

def Albums(request):

    

    A1 = Albumss
    return render(request, "music/album.html",{

        "Albums": A1

    })

def album_view(request, album):

    album_name = album

    song = Songs.objects.filter(Albums = album).order_by('Title')
   
    return render(request, 'music/album_view.html', {
        "songs": song,
        "album": album_name

    })


@login_required
def Liked(request):

    

    song = Songs.objects.all().order_by("Title")

    return render(request, 'music/Liked.html', {
        "songs": song,
        

    })



@login_required
def like(request, song_id):

    user = request.user

    song = Songs.objects.get(id = song_id)


    song_likers = song.liked_by.all()

    if user in song_likers:
        change = False
        song.liked_by.remove(user)
    else:
        change = True
        song.liked_by.add(user)
    song.save()
    return JsonResponse({"liked": change, "likes_count": song.liked_by.count()}, status= 200)



def song(request, song_id):

    song = Songs.objects.get(id = song_id)

    return render(request, 'music/song.html', {
        "song": song,
        

    })
