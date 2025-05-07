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
    os.environ['SPOTIPY_CLIENT_ID'] = '2341525e14cc4f578e733d1d6a0a468a'
    os.environ['SPOTIPY_CLIENT_SECRET'] = '5a00a83d871045d5a27ffefedfbd0c04'
    os.environ['SPOTIPY_REDIRECT_URI'] = 'http://127.0.0.1:8000/callback'

    # Create your views here.

    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id='2341525e14cc4f578e733d1d6a0a468a',
            client_secret='5a00a83d871045d5a27ffefedfbd0c04'
        )
    )

    current_user = request.session.get("current_user")  # Get from session
    profile = Profile.objects.get(user=current_user)
    user = User.objects.get(email=current_user)
    username = user.name

    # Fetch Liked Playlists
    playlist_dict = {}
    liked_playlists = profile.liked_playlist
    playlists = Playlist.objects.filter(playlistID__in=liked_playlists)

    for playlist in playlists:
        # Get the main song details for the playlist title
        main_song_id = playlist.songID
        try:
            main_track = sp.track(main_song_id)
            playlist_title = f"{main_track['name']} by {main_track['artists'][0]['name']}"
        except SpotifyException:
            playlist_title = f"Playlist {playlist.playlistID}"
            
        playlist_dict[playlist.playlistID] = {
            "title": playlist_title,
            "songs": []
        }

        # Add the main song as the first song in the list
        try:
            main_song_details = {
                "spotify_id": main_song_id,
                "title": main_track["name"],
                "artist": ", ".join([artist["name"] for artist in main_track["artists"]]),
                "image_url": main_track["album"]["images"][0]["url"] if main_track["album"]["images"] else "",
                "preview_url": main_track.get("preview_url", ""),
            }
            playlist_dict[playlist.playlistID]["songs"].append(main_song_details)
        except:
            pass  # Skip if we already had an error above

        # Add recommended songs
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
        # Get the main song details for the playlist title
        main_song_id = playlist.songID
        try:
            main_track = sp.track(main_song_id)
            playlist_title = f"{main_track['name']} by {main_track['artists'][0]['name']}"
        except SpotifyException:
            playlist_title = f"Playlist {playlist.playlistID}"
            
        history_dict[playlist.playlistID] = {
            "title": playlist_title,
            "songs": []
        }

        # Add the main song as the first song in the list
        try:
            main_song_details = {
                "spotify_id": main_song_id,
                "title": main_track["name"],
                "artist": ", ".join([artist["name"] for artist in main_track["artists"]]),
                "image_url": main_track["album"]["images"][0]["url"] if main_track["album"]["images"] else "",
                "preview_url": main_track.get("preview_url", ""),
            }
            history_dict[playlist.playlistID]["songs"].append(main_song_details)
        except:
            pass  # Skip if we already had an error above

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
        playlist_name = data.get("playlist_name", "BeatBliss Playlist")
        user = request.session.get("current_user")
        token_info = request.session.get("spotify_token")
        spotify_user_id = request.session.get("spotify_user_id")
        
        if not token_info or not spotify_user_id:
            # If user is not authenticated with Spotify, redirect to auth
            from recommApp.views import loginauth
            auth_url = loginauth(request)._headers['location'][1]
            return JsonResponse({
                "status": "auth_required", 
                "message": "Please log in to Spotify first",
                "auth_url": auth_url
            })
        
        try:
            sp = spotipy.Spotify(auth=token_info["access_token"])
            playlist = Playlist.objects.get(playlistID=plid)

            track_uris = []
            track_uris.append(f"spotify:track:{playlist.songID}")
            for song_id in playlist.recommSongs:
                if song_id:  # Skip empty IDs
                    track_uris.append(f"spotify:track:{song_id}")  # Spotify URIs format

            # Create a new playlist in the user's Spotify account
            new_playlist = sp.user_playlist_create(
                user=spotify_user_id,
                name=playlist_name,
                public=False,
                description="Recommended songs playlist from BeatBliss"
            )

            sp.playlist_add_items(new_playlist['id'], track_uris)

            # Add to liked playlists if not already there
            profile = Profile.objects.get(user=user)
            if plid not in profile.liked_playlist:
                profile.liked_playlist.append(plid)
                profile.save()
                
            return JsonResponse({
                "status": "success", 
                "message": "Playlist added to Spotify!",
                "playlist_id": new_playlist['id'],
                "playlist_url": new_playlist['external_urls']['spotify']
            })
            
        except Playlist.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Playlist not found"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
        
def signout(request):
    # Clear all session data
    request.session.flush()
    # Redirect to home page
    return redirect('home')