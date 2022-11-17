from django.shortcuts import render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from googleapiclient.discovery import build
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from .models import User, Channel

#Redirect URL for login decorator 
login_url = "login"
API_KEY = 'AIzaSyByFjMf9KMmwpeyzIwXYVfaD4UKOVjFoOI'
def index(request):
    return render(request, "capstone/index.html")

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        #Checking passwords match
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "capstone/register.html",{
                "message":"Passwords must match."
            })
        #Try to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "capstone/register.html",{
                "message":"Username is taken."
            })
        #Login the user
        login(request,user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "capstone/register.html")

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
            return render(request, "capstone/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "capstone/login.html")
    

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def callYoutube(channel):
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    findDetails = youtube.channels().list(
        part='snippet,statistics,contentDetails',
        forUsername=channel
    )
    response = findDetails.execute()
    if int(response.get("pageInfo").get("totalResults")) == 0:
        findDetails2 = youtube.channels().list(
            part='snippet,statistics,contentDetails',
            id=channel
        )
        response = findDetails2.execute()

    return response
#Searching for channel
@login_required(login_url=login_url)
def search_channel(request):
    info,title,img,desc,message,channel_id,latest_vids=["" for _ in range(7)]
    subs,views,vids=[0 for _ in range(3)]
    channel=""
    
    if request.method == 'POST' and 'getChannelname' in request.POST:
        channel = request.POST["channel_name"]
    if request.method == 'POST' and 'getChannelid' in request.POST:
        channel = request.POST["channel_id"]  
    if channel != "":
        info = callYoutube(channel)
        if info['pageInfo'].get("totalResults"):
            for item in info['items']:
                playlist_id = item['contentDetails']['relatedPlaylists']['uploads']
                latest_vids = youtubePlaylists(playlist_id)
                channel_id = item['id']
                subs = f"{int(item['statistics']['subscriberCount']):,}"
                views = f"{int(item['statistics']['viewCount']):,}"
                vids = f"{int(item['statistics']['videoCount']):,}"
                img = item['snippet']['thumbnails']['default']['url']
                title = item['snippet']['title']
                desc = item['snippet']['description']
        else:
            message = "Could not find a channel"

    user = User.objects.filter(pk=request.user.id)
    channel_ids = []
    for channel in Channel.objects.values_list('channel_id'):
        channel_ids.append(channel[0])
    return render(request, "capstone/index.html",{
        "message":message,
        "id":channel_id,
        "channel_info": title,
        "img":img,
        "subs":subs,
        "views":views,
        "vids":	vids,
        "desc":desc,
        "link":f"https://www.youtube.com/channel/{channel_id}",
        "latest":latest_vids,
        "savedChannels":channel_ids
    })

def youtubePlaylists(playlist_id):
    youtube = build('youtube', 'v3', developerKey=API_KEY)
    findPlaylist = youtube.playlistItems().list(
        part='snippet',
        playlistId= playlist_id,
        maxResults=9,
    )
    playlist = findPlaylist.execute()
    test = []
    for videos in playlist['items']:
        test.append(videos['snippet']['resourceId']['videoId'])
        
    return test

@csrf_exempt
@login_required(login_url=login_url)
def save(request):
    if request.method != "POST":
        return JsonResponse({"error":"Post request required"},status=400)

    data = json.loads(request.body)
    pfp = data.get("pfp","")
    title = data.get("title","")
    subs = int(data.get("subs","").replace(",",""))
    views = int(data.get("views","").replace(",",""))
    vids = int(data.get("vids","").replace(",",""))
    channel_id = data.get("channel_id","")

    user = User.objects.get(pk=request.user.id)
    if not Channel.objects.filter(channel_id=channel_id).exists():
        channel = Channel(user=user,title=title,img=pfp,subs=subs,views=views,videos=vids,channel_id=channel_id)
        channel.save()
    return JsonResponse({"message":"Successfully added youtuber."},status=200)

def watchlist(request):
    #Get current user
    user = User.objects.get(pk=request.user.id)
    channels = Channel.objects.filter(user=user)
    print("hello2")
    if request.POST:
        channelID = request.POST['yeet']
        Channel.objects.filter(id=channelID).delete()
        return render(request, "capstone/watchlist.html", {
            "channels":channels
        })

    return render(request, "capstone/watchlist.html",{
        "channels":channels
    })

@csrf_exempt
def remove(request):
    print("Hello")
    if request.method != "POST":
        return JsonResponse({"error":"Post request required"},status=400)

    data = json.loads(request.body)
    channel_id = data.get("channel_id","")
    user = User.objects.get(pk=request.user.id)
    Channel.objects.filter(channel_id=channel_id).delete()
    return JsonResponse({"message":"Successfully removed youtuber."},status=200)