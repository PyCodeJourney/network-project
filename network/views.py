import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import *


def index(request):
    posts_list = Post.objects.all()
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "network/index.html",
        {"page_obj": page_obj},
    )


def post(request):
    body = request.POST["post_body"]
    post = Post.objects.create(user=request.user, body=body)
    post.save()
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url="/login")
def profile(request, user_id):
    profile_owner = User.objects.get(pk=user_id)
    posts_list = Post.objects.filter(user=profile_owner)
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "network/profile.html",
        {
            "page_obj": page_obj,
            "profile_owner": profile_owner,
            "is_profile_owner": profile_owner == request.user,
            "is_follower": request.user.following.filter(
                following_user=profile_owner
            ).exists(),
            "followings_count": profile_owner.following.count(),
            "followers_count": profile_owner.followers.count(),
        },
    )


@login_required(login_url="/login")
def follow(request, user_id):
    profile_owner = User.objects.get(pk=user_id)
    entry = UserFollowing.objects.create(
        user=request.user, following_user=profile_owner
    )
    entry.save()
    return HttpResponseRedirect(reverse("profile", args=(user_id,)))


@login_required(login_url="/login")
def unfollow(request, user_id):
    profile_owner = User.objects.get(pk=user_id)
    UserFollowing.objects.filter(
        user=request.user, following_user=profile_owner
    ).delete()
    return HttpResponseRedirect(reverse("profile", args=(user_id,)))


@login_required(login_url="/login")
def following(request):
    following = UserFollowing.objects.filter(user=request.user).values("following_user")
    posts_list = Post.objects.filter(user__in=following)
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "network/following.html",
        {"page_obj": page_obj},
    )


@login_required(login_url="/login")
def edit_post(request, post_id):
    if request.method == "PUT":
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        post.body = json.loads(request.body)["body"]
        post.save()
        return JsonResponse({"message": "Post updated successfully."})
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)


@login_required(login_url="/login")
def like_post(request, post_id):
    if request.method == "POST":
        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        liked = json.loads(request.body)["liked"]
        like_button_text = "Like"
        if liked:
            post.likes.add(request.user)
            like_button_text = "Dislike"
        else:
            post.likes.remove(request.user)
        return JsonResponse(
            {
                "message": "Action completed successfully",
                "likes_count": post.likes.count(),
                "like_button_text": like_button_text,
            }
        )
    else:
        return JsonResponse({"error": "Error processing action"}, status=400)


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
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
