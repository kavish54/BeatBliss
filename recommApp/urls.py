from django.urls import path
from . import views

urlpatterns = [
    path('recommender/',views.recomHome,name='recHome'),
    path('logres/',views.loginauth,name='loginauth'),
    path('callback/',views.spotify_callback,name='spotify_callback'),
    path("autocomplete/", views.spotify_autocomplete, name="spotify-autocomplete"),
    path("results/<str:sid>/", views.show_recommendations, name="recResult"),
    path("popup/",views.show_popup,name="recSpotifyPopUp"),
    path("spotify-login/", views.spotify_login, name="spotify-login"),
    path("results/<str:sid>/",views.show_recommendations,name="recResult"),
    path("added/<str:plid>/",views.add_playlist_spotify,name="add_playlist"),
    path("like-song/", views.like_song, name="like_song"),  # New URL for liking a song
    path('like-playlist/', views.like_playlist, name='like_playlist'),
]



