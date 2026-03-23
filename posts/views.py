from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from .forms import PostForm
from .models import Category
from .models import Post, Tag
from django import template
from .forms import PostForm
from django.shortcuts import redirect
from .models import Like
from .models import Comment
from .forms import CommentForm
from django.http import JsonResponse

# Create your views here.
@login_required
def post_list(request):

    posts = Post.objects.filter(
        status="published"
    ).select_related("author", "category").prefetch_related("tags")

    context = {"posts": posts}

    return render(request, "posts/post_list.html",context)

def post_detail(request, slug):

    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()
    form = CommentForm()

    is_liked = False
    if request.user.is_authenticated:
        is_liked = post.likes.filter(user=request.user).exists()

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)

            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = request.user
                comment.post = post
                comment.save()

                return redirect("post_detail", slug=slug)

    return render(request, "posts/post_detail.html", {
        "post": post,
        "comments": comments,
        "form": form,
        "is_liked": is_liked   # ✅ pass to template
    })

@login_required
def dashboard(request):

    user = request.user

    if user.is_superuser or user.groups.filter(name="Editors").exists():
        posts = Post.objects.all()

    elif user.groups.filter(name="Authors").exists():
        posts = Post.objects.filter(author=user)

    else:
        return redirect("post_list")  # Reader cannot access dashboard

    return render(request, "dashboard/dashboard.html", {"posts": posts})
# Editor → see all posts
# Author → see own posts
# Reader → see published posts



@login_required
def my_posts(request):

    user = request.user

    if user.is_superuser or user.groups.filter(name="Editors").exists():
        posts = Post.objects.all()  # can see all

    elif user.groups.filter(name="Authors").exists():
        posts = Post.objects.filter(author=user)  # only their posts

    else:
        return redirect("post_list")  # readers blocked

    return render(request, "dashboard/my_posts.html", {"posts": posts})

@login_required
def create_post(request):

    # ✅ Allow superuser ALSO
    if not (
        request.user.is_superuser or
        request.user.groups.filter(name__in=["Authors", "Editors"]).exists()
    ):
        return redirect("post_list")

    if request.method == "POST":

        form = PostForm(request.POST, request.FILES)

        if form.is_valid():

            post = form.save(commit=False)
            post.author = request.user
            post.save()

            return render(request,'dashboard/my_posts.html')

    else:
        form = PostForm()

    return render(request, "dashboard/create_post.html", {"form": form})

@login_required
def categories(request):

    user = request.user

    # Restrict access
    if not (
        user.is_superuser or
        user.groups.filter(name="Editors").exists() or
        user.groups.filter(name="Authors").exists()
    ):
        return redirect("post_list")
    
    if request.method== "POST":
        name  = request.POST.get("name")

        if name:
                if not Category.objects.filter(name__iexact=name).exists():
                    Category.objects.create(name=name)

        return redirect("categories")

    categories = Category.objects.all()

    return render(request, "dashboard/categories.html", {
        "categories": categories
    })

@login_required
def edit_post(request, pk):

    post = get_object_or_404(Post, pk=pk)

    #  Permission check
    if not (
        request.user.groups.filter(name="Authors").exists() or
        request.user.is_superuser or
        request.user.groups.filter(name="Editors").exists()
    ):
        return redirect("post_list")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            return redirect("post_detail", slug=post.slug)

    else:
        form = PostForm(instance=post)

    return render(request, "dashboard/edit_post.html", {"form": form, "post": post})

@login_required
def delete_post(request, pk):

    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return redirect("post_list")

    post.delete()

    return redirect("my_posts")

@login_required

def logout(request):
    logout(request)
    return redirect('')

def trya(request):
    return render(request,'try.html')

from .models import Tag

@login_required
def tags(request):

    user = request.user

    #  permission
    if not (
        user.is_superuser or
        user.groups.filter(name="Editors").exists() or
        user.groups.filter(name="Authors").exists()
    ):
        return redirect("post_list")

    #  create tag
    if request.method == "POST":
        name = request.POST.get("name")

        if name:
            if not Tag.objects.filter(name__iexact=name).exists():
                Tag.objects.create(name=name)

        return redirect("tags")

    tags = Tag.objects.all()

    return render(request, "dashboard/tags.html", {
        "tags": tags
    })




from django.http import JsonResponse

@login_required
def toggle_like(request, pk):

    post = get_object_or_404(Post, pk=pk)

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        like.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        "liked": liked,
        "count": post.likes.count()
    })


@login_required
def profile(request):

    user = request.user

    if request.method == "POST":

        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.bio = request.POST.get("bio")

        if request.FILES.get("profile_image"):
            user.profile_image = request.FILES.get("profile_image")

        user.save()

        return redirect("profile")   # ✅ THIS FIXES REDIRECT

    return render(request, "dashboard/profile.html", {
        "user": user
    })