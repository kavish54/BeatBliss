from django.conf import settings
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render,redirect
import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyOAuth,SpotifyClientCredentials
from django.http import HttpResponse, JsonResponse

from loginApp.forms import User
from recommApp.models import Playlist
from recommApp.utils.recomFinder import load_knn_model, recommend_songs, train_and_save_knn_model

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

def recomHome(request):
    return render(request,'recommApp/spotify-login.html',context = {})

def loginauth(request):
    scope = "playlist-modify-private playlist-modify-public user-library-read user-read-email"
    auth = SpotifyOAuth(scope=scope)

    auth_url = auth.get_authorize_url()

    return redirect(auth_url)

def spotify_callback(request):
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
            'token':token_info,
            'user':user,
            'playlist':playlists
        }
        return render(request,'recommApp/recom-home.html',context)
    
def spotify_autocomplete(request):
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

def show_recommendations(request,sid):

    data_path = os.path.join(settings.MEDIA_ROOT, "datasets/recom_songs.csv")
    merged_df = pd.read_csv(data_path)

    nn_model, feature_matrix = load_knn_model()
    if nn_model is None:
        nn_model, feature_matrix = train_and_save_knn_model(merged_df)

    # song_name = "The Middle" 
    recommendations = recommend_songs(sid, merged_df, nn_model, feature_matrix, 5)
    suggested = []
    
    for song in recommendations:
        suggested.append(song["song_id"])

    user_instance = User.objects.get(email='kavish@gmail.com')

    playlist = Playlist.objects.create(
        user = user_instance,
        songID = sid,
        recommSongs=list(suggested)
    )
    playlist.save()
    
    context = {
        "sid" : sid,
        "recommendations" : recommendations,
        "playlist_id" : playlist.playlistID,
    }
    return render(request,'recommApp/recom-result.html',context=context)

def add_playlist_spotify(request,plid):
    token_info = request.session.get("spotify_token")
    spotify_user_id = request.session.get("spotify_user_id")

    if not token_info or not spotify_user_id:
        return HttpResponse("User not authenticated with Spotify", status=401)
    
    sp = spotipy.Spotify(auth=token_info["access_token"])

    playlist = Playlist.objects.get(playlistID=plid)

    track_uris = []
    for song_id in playlist.recommSongs:
        track_uris.append(f"spotify:track:{song_id}")  # Spotify URIs format
    track_uris.append(f"spotify:track:{playlist.songID}")
    print("Track URIs:", track_uris)

    # Create a new playlist in the user's Spotify account
    new_playlist = sp.user_playlist_create(
        user=spotify_user_id,
        name=f"BeatBliss: {playlist.songID}",
        public=False,
        description="Recommended songs playlist from BeatBliss"
    )

    sp.playlist_add_items(new_playlist['id'], track_uris)

    return HttpResponse(f"<h1>Added Playlist to Spotify!</h1>Playlist ID: {new_playlist['id']}<br>Tracks: {track_uris}")