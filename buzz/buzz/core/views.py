from django import forms
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .models import Post, Comment, Follow, Profile

User = get_user_model()

def with_counts(qs):
    return qs.select_related("author").annotate(nlikes=Count("likes", distinct=True), ncomments=Count("comments", distinct=True))

def liked_ids(request):
    return set(request.user.liked_posts.values_list("id", flat=True)) if request.user.is_authenticated else set()

def feed(request):
    tab = "all"
    posts = Post.objects.all()
    if request.user.is_authenticated and request.GET.get("tab") != "all":
        tab = "following"
        ids = list(request.user.following.values_list("following_id", flat=True)) + [request.user.id]
        posts = posts.filter(author_id__in=ids)
    return render(request, "core/feed.html", {"posts": with_counts(posts)[:50], "tab": tab, "liked_ids": liked_ids(request)})

@login_required
@require_POST
def post_create(request):
    text = request.POST.get("text", "").strip()[:280]
    if text: Post.objects.create(author=request.user, text=text)
    return redirect(request.POST.get("next") or "feed")

def post_detail(request, pk):
    post = get_object_or_404(with_counts(Post.objects.all()), pk=pk)
    if request.method == "POST":
        if not request.user.is_authenticated: return redirect("login")
        text = request.POST.get("text", "").strip()[:280]
        if text: Comment.objects.create(post=post, author=request.user, text=text)
        return redirect("post_detail", pk=pk)
    return render(request, "core/post_detail.html", {"p": post, "comments": post.comments.select_related("author"), "liked_ids": liked_ids(request)})

@login_required
@require_POST
def like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(pk=request.user.pk).exists(): post.likes.remove(request.user); liked = False
    else: post.likes.add(request.user); liked = True
    return JsonResponse({"liked": liked, "count": post.likes.count()})

@login_required
@require_POST
def post_delete(request, pk):
    get_object_or_404(Post, pk=pk, author=request.user).delete()
    return redirect("feed")

def profile(request, username):
    u = get_object_or_404(User, username=username)
    me = request.user
    return render(request, "core/profile.html", {
        "u": u, "posts": with_counts(u.posts.all()), "liked_ids": liked_ids(request),
        "nfollowers": u.followers.count(), "nfollowing": u.following.count(),
        "is_following": me.is_authenticated and Follow.objects.filter(follower=me, following=u).exists()})

@login_required
@require_POST
def follow(request, username):
    u = get_object_or_404(User, username=username)
    if u == request.user: return JsonResponse({"error": "self"}, status=400)
    rel, created = Follow.objects.get_or_create(follower=request.user, following=u)
    if not created: rel.delete()
    return JsonResponse({"following": created, "followers": u.followers.count()})

@login_required
def people(request):
    mine = set(request.user.following.values_list("following_id", flat=True))
    users = User.objects.exclude(pk=request.user.pk).annotate(nfollowers=Count("followers"))
    return render(request, "core/people.html", {"users": users, "mine": mine})

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=40, required=False)
    last_name = forms.CharField(max_length=40, required=False)
    bio = forms.CharField(max_length=160, required=False, widget=forms.Textarea(attrs={"rows": 3}))
    location = forms.CharField(max_length=60, required=False)

@login_required
def edit_profile(request):
    u = request.user
    form = ProfileForm(request.POST or None, initial={"first_name": u.first_name, "last_name": u.last_name, "bio": u.profile.bio, "location": u.profile.location})
    if request.method == "POST" and form.is_valid():
        d = form.cleaned_data
        u.first_name, u.last_name = d["first_name"], d["last_name"]; u.save()
        u.profile.bio, u.profile.location = d["bio"], d["location"]; u.profile.save()
        return redirect("profile", username=u.username)
    return render(request, "core/edit_profile.html", {"form": form})

def register(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.save()); return redirect("feed")
    return render(request, "registration/register.html", {"form": form})
