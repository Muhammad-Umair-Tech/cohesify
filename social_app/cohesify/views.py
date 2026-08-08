from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import models
from .utils import structures as strc
from .utils import sorting, helpers

friends_linked_list = strc.LinkedList()
posts_queue = strc.Queue()
# These stacks contain (action, post.id). Action can be
# "like" or "unlike". Every time the user likes/unlikes a
# post on home, a tuple is pushed in the undo stack, and
# the redo stack is cleared.
home_like_undo = strc.Stack()
home_like_redo = strc.Stack()

deleted_posts_stack = strc.Stack()
deleted_likes_stack = strc.Stack()
deleted_comments_stack = strc.Stack()

# Create your views here.
@login_required(login_url="login")
def index(request):
    posts_queryset = models.Post.objects.all()
    posts = [p for p in posts_queryset]
    sorting.sort_by_trend(posts)
    
    if request.method == "GET":
        sorting_value = request.GET.get("filter")
        if sorting_value == "oldest":
            posts = sorting.mergesort_queryset(posts) # mergesort for posts
        elif sorting_value == "latest":
            posts = sorting.mergesort_descending_queryset(posts) # mergesort for posts
        elif sorting_value == "trending":
            sorting.sort_by_trend(posts) # insertion sort
        elif sorting_value == "images":
            posts = [p for p in posts if p.is_photo]
            sorting.sort_by_trend(posts) # insertion sort
        elif sorting_value == "videos":
            posts = [p for p in posts if p.is_video]
            sorting.sort_by_trend(posts) # insertion sort

    return render(request, "cohesify/index.html", {
        "home_selected": True,
        "posts": posts,
        "liked_posts": request.user.liked_posts,
        "friends": request.user.friends.all()
    })


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        if not username or not password:
            return render(request, "cohesify/login.html", {
                "username": username,
                "password": password,
                "message": "Please fill in all the fields."
            })
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            friends_linked_list.load_all_friends(user) # Data loaded to linked list
            posts_queue.load_all_posts(user) # Data loaded in queue

            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "cohesify/login.html", {
                "message": "Incorrect username or password."
            })
    else:    
        return render(request, "cohesify/login.html")


def logout_view(request):

    friends_linked_list.head = None # Linked list cleared
    posts_queue.head = None # Queue cleared

    # Clear stacks
    helpers.clear_media_in_undo(deleted_posts_stack)
    deleted_likes_stack.clear_stack()
    deleted_comments_stack.clear_stack()
    home_like_undo.clear_stack()
    home_like_redo.clear_stack()

    logout(request)
    return HttpResponseRedirect(reverse("login"))


def sign_up(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]

        if not username or not email or not password or not confirmation or not first_name or not last_name:
            return render(request, "cohesify/sign_up.html", {
                "username": username,
                "email": email,
                "password": password,
                "confirmation": confirmation,
                "first_name": first_name,
                "last_name": last_name,
                "message": "Please fill in all the fields."
            })
        
        if password != confirmation:
            return render(request, "cohesify/sign_up.html", {
                "username": username,
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "message": "Password and confirmation must match."                
            })
        
        try:
            user = models.User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
            user.save()
        except IntegrityError:
            return render(request, "cohesify/sign_up.html", {
                "email": email,
                "password": password,
                "confirmation": confirmation,
                "first_name": first_name,
                "last_name": last_name,
                "message": "Username already taken."
            })
        login(request, user)

        friends_linked_list.load_all_friends(user) # Data loaded to linked list
        posts_queue.load_all_posts(user) # Data loaded in queue

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "cohesify/sign_up.html")


@login_required(login_url="login")
def friends(request):
    if request.method == "POST":
        id = request.POST["id"]
        action_type = request.POST["action_type"]
        redirect_view = request.POST["redirect_view"]
        target_user = models.User.objects.get(id=id)
        if action_type == "add":
            friends_linked_list.add_friend(target_user) # Added to linked list
            request.user.friends.add(target_user) 
        elif action_type == "remove":
            friends_linked_list.remove_friend(target_user.username) # Removed from linked list
            request.user.friends.remove(target_user)

        if redirect_view == "search":
            keyword = request.POST["keyword"]
            return HttpResponseRedirect(reverse("search") + f"?keyword={keyword}")
        
        return HttpResponseRedirect(reverse(redirect_view))

    all_users = models.User.objects.all()
    friends_arr = request.user.friends.all()
    to_discover = []
    for u in all_users:
        if u.username != request.user.username:
            if u not in friends_arr:
                to_discover.append(u)

    if request.method == "GET":
        sorting_value = request.GET.get("filter")
        if sorting_value == "ascending":
            friends_arr = request.user.friends.order_by("username")
            sorting.quick_sort(to_discover, 0, len(to_discover) - 1) # quicksort
        elif sorting_value == "descending":
            friends_arr = request.user.friends.order_by("-username")
            sorting.quick_sort_descending(to_discover, 0, len(to_discover) - 1) # quicksort

    return render(request, "cohesify/friends.html", {
        "friends_selected": True,
        "friends": friends_arr,
        "to_discover": to_discover
    })


@login_required(login_url="login")
def profile(request):
    friends_arr = request.user.friends.all()
    posts = request.user.posts.all()
    liked_posts = request.user.liked_posts

    if request.method == "POST":
        form_type = request.POST["form_type"]
        if form_type == "new_profile_picture":
            profile_picture = request.FILES.get("profile_picture")
            if profile_picture is not None:
                request.user.profile_picture = profile_picture
                request.user.save()
                return HttpResponseRedirect(reverse("profile"))
        elif form_type == "remove_friend":
            id = request.POST.get("id")
            if id is not None:
                target_user = models.User.objects.get(id=id)
                friends_linked_list.remove_friend(target_user.username) # Removed from linked list
                request.user.friends.remove(target_user)
                return HttpResponseRedirect(reverse("profile"))
        elif form_type == "new_post":
            caption = request.POST["caption"]
            media = request.FILES.get("media")
            if caption is None or caption == "":
                return render(request, "cohesify/profile.html", {
                    "profile_selected": True,
                    "friends": friends_arr,
                    "create_post_error": "Please enter a caption."
                })
            if media is None:
                return render(request, "cohesify/profile.html", {
                    "profile_selected": True,
                    "friends": friends_arr,
                    "create_post_error": "Please upload a file."
                })                
            post = models.Post(author=request.user, caption=caption, media=media)
            posts_queue.enqueue(post) # Post enqueued
            post.save()
            return HttpResponseRedirect(reverse("profile"))
        elif form_type == "delete_post":
            id = request.POST["id"]
            post = models.Post.objects.get(id=id)
            to_del_likes = [like for like in post.likes.all()]    # NEWWWW
            deleted_likes_stack.push(to_del_likes)
            to_del_comments = [c for c in post.comments.all()]
            deleted_comments_stack.push(to_del_comments)
            deleted_posts_stack.push(post)

            post.delete()
            posts_queue.remove(id) # Remove from queue
            return HttpResponseRedirect(reverse("profile"))
        

        elif form_type == "undo_delete": # NEWWWW
            if not deleted_posts_stack.is_empty:
                to_undo = deleted_posts_stack.pop()
                to_undo_likes = deleted_likes_stack.pop()
                to_undo_comments = deleted_comments_stack.pop()

                to_undo.pk = None # Forces Django to assign a new PK
                to_undo.save()

                for like in to_undo_likes:
                    like.pk = None
                    like.post = to_undo
                    like.save()
                for comment in to_undo_comments:
                    comment.pk = None
                    comment.post = to_undo
                    comment.save()
                
                posts_queue.enqueue(to_undo)
            return HttpResponseRedirect(reverse("profile"))
        
    posts = sorting.mergesort_descending_queryset(posts)

    if request.method == "GET":
        sorting_value = request.GET.get("filter")
        if sorting_value == "ascending":
            friends_arr = request.user.friends.order_by("username")
        elif sorting_value == "descending":
            friends_arr = request.user.friends.order_by("-username")
        elif sorting_value == "oldest":
            posts = sorting.mergesort_queryset(posts) # mergesort for posts
        elif sorting_value == "latest":
            posts = sorting.mergesort_descending_queryset(posts) # mergesort for posts

    return render(request, "cohesify/profile.html", {
        "profile_selected": True,
        "friends": friends_arr,
        "posts": posts,
        "liked_posts": liked_posts
    })


@login_required(login_url="login")
def posts(request):
    if request.method == "POST":
        form_type = request.POST.get("form_type")
        redirect_view = request.POST["redirect_view"]
        if form_type == "like_post":
            id = request.POST["id"]
            post = models.Post.objects.get(id=id)
            post_likes = post.likes.all()
            post_likers = [u.liker for u in post_likes]
            if request.user not in post_likers:                
                like = models.Like(liker=request.user, post=post)
                
                if redirect_view == "index":
                    home_like_undo.push(("like", id))
                    home_like_redo.clear_stack()

                like.save()
            else:
                prev_like = models.Like.objects.filter(post=post, liker=request.user)
                prev_like.delete()

                if redirect_view == "index":
                    home_like_undo.push(("unlike", id))
                    home_like_redo.clear_stack()

            return HttpResponseRedirect(reverse(redirect_view))
    
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url="login")
def search(request):
    keyword = request.GET.get("keyword")

    if keyword is not None and keyword != "":
        keword = keyword.lower()
        users = models.User.objects.all()
        filtered_users = [u for u in users if keyword in u.username.lower() or u.username.lower() in keyword]

        posts = models.Post.objects.all()
        filtered_posts = [p for p in posts if keyword in p.caption.lower() or p.caption.lower() in keyword]

        return render(request, "cohesify/search.html", {
            "search_selected": True,
            "keyword": keyword,
            "users": filtered_users,
            "posts": filtered_posts,
            "liked_posts": request.user.liked_posts,
            "friends": request.user.friends.all()
        })
    
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url="login")
def comments(request, post_id):
    if request.method == "POST":
        action_type = request.POST["action_type"]
        if action_type == "add_comment":
            comment_text = request.POST["comment_text"]
            redirect_view = request.POST["redirect_view"]
            if comment_text != "":
                post = models.Post.objects.get(id=post_id)
                comment = models.Comment(author=request.user, post=post, text=comment_text)
                comment.save()
                return HttpResponseRedirect(reverse("comments", args=[post_id]) + f"?redirect_view={redirect_view}")

    # If no redirect_view GET parameter, redirect to index
    redirect_view = request.GET.get("redirect_view")
    if redirect_view is None:
        redirect_view = "index"

    posts = models.Post.objects.all()
    post_ids = [p.id for p in posts]
    if post_id not in post_ids:
        return render(request, "cohesify/comments.html", {
            "message": "Invalid post ID.",
            "post_id": post_id,
            "redirect_link": reverse(redirect_view),
            "redirect_view": redirect_view
        })
    post = models.Post.objects.get(id=post_id)
    comments = post.comments.all()
    return render(request, "cohesify/comments.html", {
        "comments": comments,
        "post_id": post_id,
        "redirect_link": reverse(redirect_view),
        "redirect_view": redirect_view
    })    


@login_required(login_url="login")
def undo_redo(request):
    if request.method == "POST":

        undo_action = request.POST.get("undo_action")

        if undo_action == "undo":
            if home_like_undo.is_empty:
                return HttpResponseRedirect(reverse("index"))

            action, post_id = home_like_undo.pop()
            home_like_redo.push((action, post_id))

            post = models.Post.objects.get(id=post_id)

            if action == "like":
                models.Like.objects.filter(post=post, liker=request.user).delete()
            else:
                new_like = models.Like(post=post, liker=request.user)
                new_like.save()

        if undo_action == "redo":
            if home_like_redo.is_empty:
                return HttpResponseRedirect(reverse("index"))
            action, post_id = home_like_redo.pop()
            home_like_undo.push((action, post_id))
            post = models.Post.objects.get(id=post_id)
            if action == "like":
                new_like = models.Like(post=post, liker=request.user)
                new_like.save()
            else:
                models.Like.objects.filter(post=post, liker=request.user).delete()

        return HttpResponseRedirect(reverse("index"))
    
    return HttpResponseRedirect(reverse("index"))

