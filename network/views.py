from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponseServerError, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import *
from datetime import datetime
from .serializer import PostSerializer
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
import json


def index(request):
    return render(request, "network/index.html")


def following(request, profile):
    return render(request, "network/following.html", {
        "following": True
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

@login_required
def add_post(request):
    post = request.POST['post']
    user = User.objects.filter(username = request.user.username)[0]
    new_post = Post(user = user, post = post)
    new_post.save()
    return HttpResponseRedirect(reverse("index"))


@api_view(['GET'])
def posts(request):
    following = request.GET.get("following") or None
    page = int(request.GET.get("page") or 0)
    profile = request.GET.get("profile") or None
    if following:
        # Usuario utilizando la web
        user = User.objects.filter(username = profile)[0]
        # Perfiles a los cuales el usuario sigue
        followings = Follow.objects.filter(follower = user)
        users_following = []
        for following in followings:
            users_following.append(following.profile)
        posts = Post.objects.filter(user__in=users_following).order_by('-id')
    elif profile:
        user = User.objects.filter(username = profile)[0]
        posts = Post.objects.filter(user = user).order_by('-id')
    else: 
        posts = Post.objects.all().order_by('-id')
    post = []
    for i in range(page, page + 10):
        try: 
            post.append(posts[i])
        except:
            break
    serializer = PostSerializer(post, many=True)
    return Response(serializer.data)


def total_posts(request):
    following = request.GET.get("following") or None
    profile = request.GET.get("profile") or None    
    if following:
        # Usuario utilizando la web
        user = User.objects.filter(username = profile)[0]
        # Perfiles a los cuales el usuario sigue
        followings = Follow.objects.filter(follower = user)
        users_following = []
        for following in followings:
            users_following.append(following.profile)
        posts = Post.objects.filter(user__in=users_following).order_by('-id')
    
    elif profile:
        user = User.objects.filter(username = profile)[0]
        posts = Post.objects.filter(user = user)
    else:
        posts = Post.objects.all()
    total = len(posts)
    return JsonResponse({
        'total': total
    })


def user_profile(request, profile):
    profile = User.objects.filter(username = profile)[0]
    try:
        user = User.objects.filter(username = request.user.username)[0]
    except:
        user = None
    try:
        followers = len(Follow.objects.filter(profile = profile))
    except:
        followers = 0
    try:
        following = len(Follow.objects.filter(follower = profile))
    except:
        following = 0
    try:
        follow = Follow.objects.filter(profile = profile, follower = user)
    except:
        follow = None
    return render(request, "network/profile.html", {
        "profile": profile,
        'follow': follow,
        'followers': followers,
        'following': following
    })


def add_follower(request, profile):
    profile = User.objects.filter(username = profile)[0]
    follower = User.objects.filter(username = request.user.username)[0]
    new_follower = Follow(profile = profile, follower = follower)
    new_follower.save()
    return HttpResponseRedirect(reverse('user_profile', kwargs={"profile": profile}))


def delete_follower(request,profile):
    profile = User.objects.filter(username = profile)[0]
    follower = User.objects.filter(username = request.user.username)[0]
    Follow.objects.filter(profile = profile, follower = follower).delete()
    return HttpResponseRedirect(reverse('user_profile', kwargs={"profile": profile}))


@login_required
@csrf_exempt
def update_post(request, post_id):
    try:
        post = Post.objects.filter(id = post_id)[0]
    except:
        return JsonResponse({"Error": "Publicacion no encontrada"}, status=400)
    data = json.loads(request.body)
    new_post = data.get('post')
    Post.objects.filter(id = post_id).update(post = new_post)
    return JsonResponse({ "Mensaje": "Publicacion actualizada con exito"}, status=201)


@login_required
def is_liked(request, post_id):
    # Obtenemos la publicacion
    post = Post.objects.filter(id = post_id)[0]
    # Obtenemos el usuario actual
    user = User.objects.filter(username = request.user.username)[0]
    try:
        like = Like.objects.filter(post = post, user = user)[0]
        return JsonResponse({"like": "True"})
    except:
        return JsonResponse({"like": "False"})


@login_required
def like_post(request, post_id):
    post = Post.objects.filter(id = post_id)[0]
    likes = post.like
    likes = likes + 1
    Post.objects.filter(id = post_id).update(like = likes)
    user = User.objects.filter(username = request.user.username)[0]
    new_like = Like(post = post, user = user)
    new_like.save()
    return JsonResponse({"Mensaje": "Se a dado me gusta satifactoriamente"}, status=201)


@login_required
def dislike_post(request, post_id):
    post = Post.objects.filter(id = post_id)[0]
    likes = post.like
    likes = likes - 1
    Post.objects.filter(id = post_id).update(like = likes)
    user = User.objects.filter(username = request.user.username)[0]
    Like.objects.filter(post = post, user = user).delete()
    return JsonResponse({"Mensaje": "Se sacado el me gusta satifactoriamente"}, status=201)