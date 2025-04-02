import os
from django.shortcuts import render
import spotipy
from django.conf import settings
from loginApp.models import User
from recommApp.models import Playlist
from .models import Profile
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException

def profilePage(request):
    os.environ['SPOTIPY_CLIENT_ID'] = 'cfd82609829c4df08e69069c5c37e201'
    os.environ['SPOTIPY_CLIENT_SECRET'] = '0cc553a74abf4a328b0cd70a661fd01f'
    os.environ['SPOTIPY_REDIRECT_URI'] = 'http://127.0.0.1:8000/callback'

    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id='cfd82609829c4df08e69069c5c37e201',
            client_secret='0cc553a74abf4a328b0cd70a661fd01f'
        )
    )

    current_user = request.user  # Use Django authentication system
    profile = Profile.objects.get(user=current_user)
    user = User.objects.get(email=current_user)
    username = user.name

    # Fetch Liked Playlists
    playlist_dict = {}
    liked_playlists = profile.liked_playlist
    playlists = Playlist.objects.filter(playlistID__in=liked_playlists)

    for playlist in playlists:
        playlist_dict[playlist.playlistID] = {"songs": []}

        for song_id in playlist.recommSongs:
            if not song_id:  # Skip empty IDs
                continue
            try:
                track = sp.track(song_id)  # Fetch song details
                song_details = {
                    "spotify_id": song_id,
                    "title": track["name"],
                    "artist": ", ".join([artist["name"] for artist in track["artists"]]),
                    "image_url": track["album"]["images"][0]["url"] if track["album"]["images"] else "",
                    "preview_url": track.get("preview_url", ""),
                }
                playlist_dict[playlist.playlistID]["songs"].append(song_details)
            except SpotifyException:
                print(f"recentInvalid Spotify ID: {song_id}")  # Debugging

    # Fetch Last 5 Created Playlists
    history_dict = {}
    recent_playlists = Playlist.objects.filter(user=current_user).order_by('-created_at')[:5]

    for playlist in recent_playlists:
        history_dict[playlist.playlistID] = {"songs": []}

        for song_id in playlist.recommSongs:
            if not song_id:
                continue
            try:
                track = sp.track(song_id)
                song_details = {
                    "spotify_id": song_id,
                    "title": track["name"],
                    "artist": ", ".join([artist["name"] for artist in track["artists"]]),
                    "image_url": track["album"]["images"][0]["url"] if track["album"]["images"] else "",
                    "preview_url": track.get("preview_url", ""),
                }
                history_dict[playlist.playlistID]["songs"].append(song_details)
            except SpotifyException:
                print(f"history----Invalid Spotify ID: {song_id}")

    # Fetch liked songs list
    # Fetch liked songs list
    liked_songs = {}

    for song_id in profile.liked_song_list:
        if not song_id:  # Skip empty IDs
            continue
        try:
            track = sp.track(song_id)  # Fetch song details from Spotify API
            liked_songs[song_id] = {
                "spotify_id": song_id,
                "title": track["name"],
                "artist": ", ".join([artist["name"] for artist in track["artists"]]),
                "image_url": track["album"]["images"][0]["url"] if track["album"]["images"] else "",
                "preview_url": track.get("preview_url", ""),
            }
        except SpotifyException:
            print(f"liked songs----Invalid Spotify ID: {song_id}")  # Debugging


    context = {"playlist_dict": playlist_dict, "history_dict": history_dict,"liked_songs":liked_songs,"username":username}
    return render(request, 'profileApp/profile-page.html', context)

