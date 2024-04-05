from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

def index(request):
    if request.user.is_authenticated:return redirect("dashboard")
    else:return redirect('signin')

def ytvd(request):
    if request.method == 'POST':
        url = request.POST['url']
        if 'youtube.com' in url or 'youtu.be' in url:
            from pytube import YouTube
            yt = YouTube(url)
            title = yt.title
            thumbnail = yt.thumbnail_url
            stream = yt.streams.filter(progressive=True).get_highest_resolution()
            stream.download()
            return render(request, 'ytd.html', {'title':title, 'thumbnail':thumbnail})
        
        else:messages.info(request, 'Invalid URL')
    return render(request, 'ytd.html')

def dashboard(request):
    if request.user.is_authenticated:return render(request,'dashboard.html')
    else:return redirect('signin')

def signup(request):
    if request.user.is_authenticated:return render(request,'index.html')
    elif request.method=="POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists() and User.objects.filter(email=email).exists():messages.info(request, 'Username and Email already exists')
        elif User.objects.filter(username=username).exists():messages.info(request, 'Username already exists')
        elif User.objects.filter(email=email).exists():messages.info(request, 'Email already exists')
        else:
            user = User.objects.create_user(username, email, password)
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect("dashboard")
        return redirect("signup")
    else:return render(request,'signup.html')

def signin(request):
    if request.user.is_authenticated:return redirect('dashboard')
    elif request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        if '@' in username:username = User.objects.get(email=username.lower()).username
        user = authenticate(request, username=username, password=password)
        if user:login(request, user)
        else:messages.info(request, 'User not found')
        return redirect("signin")
    return render(request,'signin.html')

def signout(request):
    if request.user.is_authenticated:logout(request)
    return redirect('signin')