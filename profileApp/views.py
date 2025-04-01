import os
from django.shortcuts import render
import spotipy

from recommApp.models import Playlist
from .models import Profile
from spotipy.oauth2 import SpotifyOAuth,SpotifyClientCredentials

# Create your views here.

def profilePage(request):
    os.environ['SPOTIPY_CLIENT_ID'] = 'cfd82609829c4df08e69069c5c37e201'
    os.environ['SPOTIPY_CLIENT_SECRET'] = '0cc553a74abf4a328b0cd70a661fd01f'
    os.environ['SPOTIPY_REDIRECT_URI'] = 'http://127.0.0.1:8000/callback'

# Create your views here.

    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id='cfd82609829c4df08e69069c5c37e201',
            client_secret='0cc553a74abf4a328b0cd70a661fd01f'
        )
    )
    current_user = request.session.get('current_user')
    profile = Profile.objects.get(user=current_user)
    liked_playlists = profile.liked_playlist

    playlist_dict = {}

    playlists = Playlist.objects.filter(playlistID__in=liked_playlists)
    for playlist in playlists:
        playlist_dict[playlist.playlistID] = {"songs": []}
        
        for song_id in playlist.recommSongs:
            track = sp.track(song_id)
            song_details = {
                "spotify_id": song_id,
                "title": track["name"],
                "artist": ", ".join([artist["name"] for artist in track["artists"]]),
                "image_url": track["album"]["images"][0]["url"] if track["album"]["images"] else "",
                "preview_url": track.get("preview_url", ""),
            }
            playlist_dict[playlist.playlistID]["songs"].append(song_details)
    
    context = {"playlist_dict": playlist_dict}
    return render(request, 'profileApp/profile-page.html',context)