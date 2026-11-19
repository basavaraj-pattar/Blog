from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from .forms import SignUpForm, PostForm, CommentForm
from .models import Post, Category, Tag, Like, Comment

def home(request):
    posts = Post.objects.filter(status=Post.Status.PUBLISHED).select_related("author", "category").prefetch_related("tags")
    query = request.GET.get("q", "").strip()
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(excerpt__icontains=query))
    return render(request, "blog/home.html", {
        "posts": posts, "query": query,
        "categories": Category.objects.all(),
        "popular_tags": Tag.objects.all()[:12],
    })

def post_detail(request, slug):
    post = get_object_or_404(Post.objects.select_related("author", "category").prefetch_related("tags"), slug=slug)
    if post.status != Post.Status.PUBLISHED and (not request.user.is_authenticated or request.user != post.author and not request.user.is_staff):
        return get_object_or_404(Post.objects.filter(status=Post.Status.PUBLISHED), slug=slug)
    form = CommentForm()
    return render(request, "blog/post_detail.html", {
        "post": post, "comment_form": form,
        "liked": request.user.is_authenticated and post.likes.filter(user=request.user).exists(),
    })

def category_posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status=Post.Status.PUBLISHED).select_related("author", "category")
    return render(request, "blog/post_list.html", {"posts": posts, "heading": category.name})

def tag_posts(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, status=Post.Status.PUBLISHED).select_related("author", "category")
    return render(request, "blog/post_list.html", {"posts": posts, "heading": f"#{tag.name}"})

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your account is ready. Welcome!")
            return redirect("dashboard")
    else:
        form = SignUpForm()
    return render(request, "registration/signup.html", {"form": form})

@login_required
def dashboard(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, "blog/dashboard.html", {"posts": posts})

@login_required
def post_create(request):
    form = PostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        form.save_m2m()
        messages.success(request, "Post saved.")
        return redirect("dashboard")
    return render(request, "blog/post_form.html", {"form": form, "heading": "Create a post"})

@login_required
def post_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You cannot edit this post.")
    form = PostForm(request.POST or None, instance=post)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Post updated.")
        return redirect("dashboard")
    return render(request, "blog/post_form.html", {"form": form, "heading": "Edit post"})

@login_required
def post_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You cannot delete this post.")
    if request.method == "POST":
        post.delete()
        messages.success(request, "Post deleted.")
        return redirect("dashboard")
    return render(request, "blog/post_confirm_delete.html", {"post": post})

@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post, comment.author = post, request.user
            comment.save()
            messages.success(request, "Comment added.")
    return redirect(post.get_absolute_url() + "#comments")

@login_required
def toggle_like(request, slug):
    post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)
    like, created = Like.objects.get_or_create(post=post, user=request.user)
    if not created:
        like.delete()
    return redirect(post.get_absolute_url())

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author != request.user and comment.post.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You cannot delete this comment.")
    post_url = comment.post.get_absolute_url() + "#comments"
    if request.method == "POST":
        comment.delete()
        messages.success(request, "Comment deleted.")
    return redirect(post_url)
