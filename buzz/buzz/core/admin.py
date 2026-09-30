from django.contrib import admin
from .models import Profile, Post, Comment, Follow
for m in (Profile, Post, Comment, Follow): admin.site.register(m)
