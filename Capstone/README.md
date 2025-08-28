# CS50 Final Project- Music App

Hello!, I’m Naveen Kumar and this README file consists of information regarding my web application MUSICLY. 

Musicly is a similar web application to Spotify(www.spotify.com)  and SoundCloud (www.soundcloud.com). This web application allows user to listen to songs online for free.


- This application is built using Django, Python and JavaScript. 

## Overview

User who aren’t logged in have permission to use limited features such as they only have access to a page where all the songs are displayed and are ready to be played, along with another page where the songs are catorogrized into different albums and clicking on an album would allow them to see and play the songs that album consists of. However, these users can register themselves anytime they want. On the other hand, users who are logged in are enabled to access additional features, for example, the user can like any song and all their liked songs are displayed on a separate page however if a user wishes to remove the song from their liked songs unlike button is always there to help them out. Can’t find your favorite song? Well that’s something logged in user wouldn’t worry about as they have an additional feature of uploading any song they like and that song would be available for all the users across the web-application. 

## Distinctiveness and Complexity

My project is different and more complex than previous projects due to following reasons:

- Instead of other files like images, my application also deals with with audio files 
- On my index page, the songs are alphabetically ordered instead of the timestamp
- It contains different models
- The CSS of this application is much better and more complex than the previous projects
- All 3 Django, Python, and JavaScript are used for creating the web-application
- The idea of this web application is completely different from the previous projects
- Users can play and hear the songs on the website 
- There’s a real-time count of the likes on the song
- As required there should be at least one model in my web application however it contains two (User and Songs)
- My web is also mobile-responsive, sizes changes according to the screen size 


## To run the server

My website can be easily run by using this command in the terminal:

```bash
  python/python3 manage.py runserver
```


## Usuable Account
If you don't want to create an account you can use these credentials and these can also be used in the /admin route

**User:** NK

**Password:** 123


## Web pages

The web pages created to make this web application are as follow:

----
Login.html
----
This page allows users who are registered to log in

---

Register.html
----

This page allows new users to register themselves

---

Index.html
----

On this page, all the songs across the web application are shown and the title, singer, and like count of the songs. Users can listen to any song they like and the users who are logged in can even like it. 

---

Layout.html
----
It has a basic layout that all other pages share. It has a nav bar with links to other pages. 

---

New_audio.html
----
This page is only available for logged-in users and on this page, the user is shown a form for uploading the new song. They have to fill out the fields such as the title of the song, singer of the song, option to select and upload music file and select an album for the song. 

---

Song.html
----
It is displayed whenever a user clicks on the song. On this page the following are displayed:
- Title
- Singer
- Song Audio
- Like count

---

Liked.html 
----
This page is only visible for the logged-in users and on this page, all the liked songs of the user are displayed. 

---

album.html
---
On this page, all the songs of a particular album are displayed. 

---

## JavaScript

Like.js 
---

Using javascript from the file users can like/unlike a post and they are displayed with the like count of the song



## Routes

The different routes in my web application are as follows:

---

- "“- default route which shows all the songs
- “Login” - where the user can log in
- “Register”- where users can register themselves 
- “Logout”- allowing users to log out
- “AddNewAudio”- here users upload a new song
- “Albums”- displays all the albums
- “albums/<str: album>”- shows all the songs in a particular album
- “Likedsongs”- shows all the songs liked by the user
- “song/<int:song_id>”- shows all the details for a particular song
- “like/<str:song_id>”- allows users to like/unlike the song
## Models

There are 2 models on my page 

---
User
---
Just normal for allowing a user to register themselves and their details

---
Songs
---

This model has the attributes that each song must contain. Its attributes are as follows:

- Title: Title of the song
- Singer: Singer of the song
- Audio: Audio file of the song
- Poster: User who uploaded the song
- Albums: List of albums according to which songs are categorized
- Liked_by: List of users who have liked the song