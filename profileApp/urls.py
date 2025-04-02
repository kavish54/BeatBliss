from django.urls import path
from .views import profilePage,like_playlist
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('profile/',profilePage,name="profile-page"),
    path('like-playlist/',like_playlist,name="like-playlist")
]
