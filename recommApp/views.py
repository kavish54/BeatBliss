from django.conf import settings
from django.shortcuts import render, redirect
import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from django.http import HttpResponse, JsonResponse
from django.contrib import messages

from loginApp.forms import User
from profileApp.models import Profile
from recommApp.models import Playlist
from recommApp.utils.recomFinder import load_knn_model, recommend_songs, train_and_save_knn_model

import json
from django.http import JsonResponse
from decouple import config

os.environ['SPOTIPY_CLIENT_ID'] = config('SPOTIPY_CLIENT_ID')
os.environ['SPOTIPY_CLIENT_SECRET'] = config('SPOTIPY_CLIENT_SECRET')
os.environ['SPOTIPY_REDIRECT_URI'] = config('SPOTIPY_REDIRECT_URI')

    # Create your views here.

sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id= config('SPOTIPY_CLIENT_ID'),
            client_secret= config('SPOTIPY_CLIENT_ID')
        )
    )

def recomHome(request):
    # if 'spotify_token' in request.session:
        # del request.session['spotify_token']
    return render(request, 'recommApp/recom-home.html', context={})

# user-library-read add in below
def loginauth(request):
    # Check if user is logged in
    if not request.session.get("current_user"):
        messages.error(request, "Please log in to connect with Spotify")
        return redirect("login")
        
    scope = "playlist-modify-private playlist-modify-public user-read-email user-library-modify user-library-read"
    auth = SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope=scope,
        # show_dialog=True
    )

    auth_url = auth.get_authorize_url()
    
    return redirect(auth_url)

def spotify_callback(request):
    # Check if user is logged in
    if not request.session.get("current_user"):
        messages.error(request, "Please log in to connect with Spotify")
        return redirect("login")
        
    auth = SpotifyOAuth(scope="user-library-read")
    
    # Get authorization code from URL parameters
    code = request.GET.get("code")
    
    if code:
        # Exchange authorization code for access token
        token_info = auth.get_access_token(code)
        
        # Save token in session (optional)
        request.session["spotify_token"] = token_info 

        sp = spotipy.Spotify(auth=token_info["access_token"])
        user = sp.current_user()
        spotify_user_id = user['id']

        request.session['spotify_user_id'] = spotify_user_id
        playlists = sp.current_user_playlists()
        
        context = {
            'token': token_info,
            'user': user,
            'playlist': playlists
        }
        return render(request, 'recommApp/recom-home.html', context)
    
def spotify_autocomplete(request):
    # Check if user is logged in
    if not request.session.get("current_user"):
        return JsonResponse({"error": "Authentication required"}, status=401)
        
    query = request.GET.get("q", "").strip().lower()

    if not query:
        return JsonResponse({"error": "No query provided"}, status=400)

    # Load the local dataset
    songsRC = pd.read_csv('media/datasets/recom_songs.csv')

    # Validate if necessary columns exist
    required_columns = {'song_id', 'song_name', 'artists'}
    if not required_columns.issubset(songsRC.columns):
        return JsonResponse({"error": "Invalid dataset format"}, status=500)

    # Filter dataset by query and limit to top 5
    filtered_songs = songsRC[songsRC['song_name'].str.lower().str.contains(query, na=False)].head(5)

    suggestions = []
    
    # Fetch details from Spotify API using song ID
    for _, item in filtered_songs.iterrows():
        song_id = item['song_id']
        
        try:
            track = sp.track(song_id)

            suggestions.append({
                "id": song_id,
                "name": track['name'],
                "artist": ", ".join(artist['name'] for artist in track['artists']),
                "album": track['album']['name'],
                "image": track['album']['images'][0]['url'] if track['album']['images'] else "",
                "spotify_url": track['external_urls']['spotify']
            })

        except Exception as e:
            # Fallback in case of Spotify API failure
            suggestions.append({
                "id": song_id,
                "name": item['song_name'],
                "artist": item['artists'],
                "album": "None",
                "image": "",
                "spotify_url": "None",
                "error": str(e)
            })

    return JsonResponse({"suggestions": suggestions})

def show_recommendations(request, sid):
    # Check if user is logged in
    if not request.session.get("current_user"):
        messages.error(request, "Please log in to view recommendations")
        return redirect("login")

    data_path = os.path.join(settings.MEDIA_ROOT, "datasets/recom_songs.csv")
    merged_df = pd.read_csv(data_path)

    nn_model, feature_matrix = load_knn_model()
    if nn_model is None:
        nn_model, feature_matrix = train_and_save_knn_model(merged_df)

    recommendations = recommend_songs(sid, merged_df, nn_model, feature_matrix, 5)

    track = sp.track(sid)

    current_song = ({
        "name": track['name'],
        "artist": ", ".join(artist['name'] for artist in track['artists']),
        "album": track['album']['name'],
        "image": track['album']['images'][0]['url'] if track['album']['images'] else "",
        "spotify_url": track['external_urls']['spotify'],
        "preview_url": track['preview_url']
    })
    suggested = []
    song_details = []
    for song in recommendations:
        track = sp.track(song["song_id"])

        song_details.append({
            "id": song["song_id"],
            "name": track['name'],
            "artist": ", ".join(artist['name'] for artist in track['artists']),
            "album": track['album']['name'],
            "image": track['album']['images'][0]['url'] if track['album']['images'] else "",
            "spotify_url": track['external_urls']['spotify'],
            "preview_url": track['preview_url']  # Added preview URL
        })
        suggested.append(song["song_id"])

    user_instance = User.objects.get(email=request.session.get("current_user"))

    playlist = Playlist.objects.create(
        user = user_instance,
        songID = sid,
        recommSongs=list(suggested)
    )
    playlist.save()
    
    context = {
        "sid": sid,
        "current": current_song,
        "recommendations": recommendations,
        "playlist_id": playlist.playlistID,
        "song_details": song_details,
    }
    return render(request, 'recommApp/recom-result.html', context=context)

def show_popup(request):
    return render(request, "recommApp/spotify-popup.html")

def spotify_login(request):  # This handles the login page
    return render(request, "recommApp/spotify-login.html")


def add_playlist_spotify(request, plid):
    # Check if user is logged in
    if not request.session.get("current_user"):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                "status": "error", 
                "message": "Please log in to add playlists"
            })
        messages.error(request, "Please log in to add playlists")
        return redirect("login")
        
    token_info = request.session.get("spotify_token")
    spotify_user_id = request.session.get("spotify_user_id")

    if not token_info or not spotify_user_id:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                "status": "error", 
                "message": "User not authenticated with Spotify"
            })
        return HttpResponse("User not authenticated with Spotify", status=401)
    
    try:
        sp = spotipy.Spotify(auth=token_info["access_token"])
        playlist = Playlist.objects.get(playlistID=plid)

        track_uris = []
        track_uris.append(f"spotify:track:{playlist.songID}")
        for song_id in playlist.recommSongs:
            track_uris.append(f"spotify:track:{song_id}")  # Spotify URIs format

        # Get custom playlist name if provided
        if request.method == "POST":
            data = json.loads(request.body)
            playlist_name = data.get("playlist_name", f"BeatBliss: {playlist.songID}")
        else:
            playlist_name = f"BeatBliss: {playlist.songID}"

        # Create a new playlist in the user's Spotify account
        new_playlist = sp.user_playlist_create(
            user=spotify_user_id,
            name=playlist_name,
            public=False,
            description="Recommended songs playlist from BeatBliss"
        )

        sp.playlist_add_items(new_playlist['id'], track_uris)
        
        # Check if this is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                "status": "success",
                "message": "Playlist added to your Spotify account!",
                "playlist_id": new_playlist['id'],
                "playlist_url": new_playlist['external_urls']['spotify']
            })
            
        # For non-AJAX requests, return the original response
        return HttpResponse(f"<h1>Added Playlist to Spotify!</h1>Playlist ID: {new_playlist['id']}<br>Tracks: {track_uris}")
        
    except Playlist.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                "status": "error",
                "message": "Playlist not found"
            })
        return HttpResponse("Playlist not found", status=404)
        
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                "status": "error",
                "message": str(e)
            })
        return HttpResponse(f"Error: {str(e)}", status=500)

def like_song(request):
    # Check if user is logged in
    if not request.session.get("current_user"):
        return JsonResponse({"status": "error", "message": "Please log in to like songs"}, status=401)
        
    if request.method == "POST":
        data = json.loads(request.body)
        song_id = data.get("song_id")
        user = request.session.get("current_user")
        token_info = request.session.get("spotify_token")
        if not token_info:
            return JsonResponse({"status": "error", "message": "User not authenticated with Spotify"}, status=401)

        sp = spotipy.Spotify(auth=token_info["access_token"])
        try:
            sp.current_user_saved_tracks_add([song_id])
            profile = Profile.objects.get(user=user)
            profile.liked_song_list.append(song_id)
            profile.save()
            return JsonResponse({"status": "success", "message": "Song added to Liked Songs"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
        
# Add this new function to your views.py file

def like_playlist(request):
    if request.method == "POST":
        data = json.loads(request.body)
        playlist_id = data.get("playlist_id")
        user_email = request.session.get("current_user")
        
        try:
            # Get the user's profile
            user_instance = User.objects.get(email=user_email)
            profile = Profile.objects.get(user=user_email)
            
            # Initialize liked_playlist if it doesn't exist
            if not hasattr(profile, 'liked_playlist') or profile.liked_playlist is None:
                profile.liked_playlist = []
            
            # Check if playlist is already liked
            if int(playlist_id) not in profile.liked_playlist:
                # Add playlist ID to liked_playlist
                profile.liked_playlist.append(int(playlist_id))
                profile.save()
                return JsonResponse({"status": "success", "message": "Playlist added to your liked playlists"})
            else:
                return JsonResponse({"status": "info", "message": "Playlist already in your liked playlists"})
                
        except User.DoesNotExist:
            return JsonResponse({"status": "error", "message": "User not found"}, status=404)
        except Profile.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Profile not found"}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=400)