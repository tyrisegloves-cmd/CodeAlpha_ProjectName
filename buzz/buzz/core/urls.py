from django.urls import path
from . import views as v
urlpatterns = [
    path("", v.feed, name="feed"),
    path("post/new/", v.post_create, name="post_create"),
    path("post/<int:pk>/", v.post_detail, name="post_detail"),
    path("post/<int:pk>/like/", v.like, name="like"),
    path("post/<int:pk>/delete/", v.post_delete, name="post_delete"),
    path("people/", v.people, name="people"),
    path("settings/profile/", v.edit_profile, name="edit_profile"),
    path("register/", v.register, name="register"),
    path("u/<str:username>/", v.profile, name="profile"),
    path("u/<str:username>/follow/", v.follow, name="follow"),
]
