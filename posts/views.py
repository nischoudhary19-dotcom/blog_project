from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from .forms import PostForm
from .models import Category
from .models import Post

# Create your views here.
@login_required
def post_list(request):

    posts = Post.objects.filter(
        status="published"
    ).select_related("author", "category").prefetch_related("tags")

    context = {"posts": posts}

    return render(request, "posts/post_list.html",context)

def post_detail(request, slug):

    post = get_list_or_404(Post, slug=slug)
    return render(request, "posts/post_detail.html", {"post":post[0]})


@login_required
def dashboard(request):

    user = request.user

    if user.is_superuser or user.groups.filter(name="Editor").exists():
        posts = Post.objects.all()

    elif user.groups.filter(name="Author").exists():
        posts = Post.objects.filter(author=user)

    else:
        return redirect("post_list")  # Reader cannot access dashboard

    return render(request, "dashboard/dashboard.html", {"posts": posts})
# Editor → see all posts
# Author → see own posts
# Reader → see published posts



@login_required
def my_posts(request):

    if not request.user.groups.filter(name="Author").exists():
        return redirect("post_list")

    posts = Post.objects.filter(author=request.user)

    return render(request, "dashboard/my_posts.html", {"posts": posts})

from .forms import PostForm
from django.shortcuts import redirect

@login_required
def create_post(request):

    # ✅ Allow superuser ALSO
    if not (
        request.user.is_superuser or
        request.user.groups.filter(name__in=["Author", "Editor"]).exists()
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

    categories = Category.objects.all()

    context = {
        "categories": categories
    }

    return render(request, "dashboard/categories.html")


@login_required
def edit_post(request, pk):

    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return redirect("post_list")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)

        if form.is_valid():
            form.save()
            return redirect("my_posts")

    else:
        form = PostForm(instance=post)

    return render(request, "dashboard/edit_post.html", {"form": form})

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