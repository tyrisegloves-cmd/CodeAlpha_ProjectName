from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = settings.AUTH_USER_MODEL

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.CharField(max_length=160, blank=True)
    location = models.CharField(max_length=60, blank=True)
    def __str__(self): return self.user.username

@receiver(post_save, sender=User)
def make_profile(sender, instance, created, **kw):
    if created: Profile.objects.create(user=instance)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    text = models.CharField(max_length=280)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["-created"]
    def __str__(self): return f"{self.author}: {self.text[:30]}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=280)
    created = models.DateTimeField(auto_now_add=True)
    class Meta: ordering = ["created"]

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    created = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together = ("follower", "following")
