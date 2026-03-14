from django.shortcuts import render, get_list_or_404
from .models import Post

# Create your views here.
def post_list(request):

    posts = Post.objects.filter(
        status="published"
    ).select_related("author", "category").prefetch_related("tags")

    context = {"posts": posts}

    return render(request, "posts/post_list.html",context)

def post_detail(request, slug):

    post = get_list_or_404(Post, slug=slug)
    return render(request, "posts/post_detail.html", {"post":post[0]})
