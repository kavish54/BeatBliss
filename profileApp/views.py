import json
import os
from django.http import JsonResponse
from django.shortcuts import redirect, render
import spotipy
from django.conf import settings
from loginApp.models import User
from recommApp.models import Playlist
from .models import Profile
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException

def profilePage(request):
    os.environ['SPOTIPY_CLIENT_ID'] = '7d014370fbc24589848407b92579c6e7'
    os.environ['SPOTIPY_CLIENT_SECRET'] = '2e0b934440ab44eab116a6b87e7ac3cf'
    os.environ['SPOTIPY_REDIRECT_URI'] = 'http://127.0.0.1:8000/callback'

    # Create your views here.

    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id='7d014370fbc24589848407b92579c6e7',
            client_secret='2e0b934440ab44eab116a6b87e7ac3cf'
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

def like_playlist(request):
    if request.method == "POST":
        data = json.loads(request.body)
        plid = data.get("pl_id")
        user = request.session.get("current_user")
        token_info = request.session.get("spotify_token")
        spotify_user_id = request.session.get("spotify_user_id")
        if not token_info:
            return JsonResponse({"status": "error", "message": "User not authenticated with Spotify"}, status=401)

        sp = spotipy.Spotify(auth=token_info["access_token"])
        print(plid+"gujaasananan")
        try:
            print(plid+"dasananan")
            playlist = Playlist.objects.get(playlistID=plid)

            track_uris = []
            track_uris.append(f"spotify:track:{playlist.songID}")
            for song_id in playlist.recommSongs:
                track_uris.append(f"spotify:track:{song_id}")  # Spotify URIs format
            print("Track URIs:", track_uris)

            # Create a new playlist in the user's Spotify account
            new_playlist = sp.user_playlist_create(
                user=spotify_user_id,
                name=f"BeatBliss: {playlist.songID}",
                public=False,
                description="Recommended songs playlist from BeatBliss"
            )

            sp.playlist_add_items(new_playlist['id'], track_uris)

            profile = Profile.objects.get(user=user)
            profile.liked_song_list.append(song_id)
            profile.save()
            return JsonResponse({"status": "success", "message": "Playlist added to spotify"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
        
def logout(request):
    # Clear all session data
    request.session.flush()
    # Redirect to home page
    return redirect('home')