from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
import librosa
from .forms import UploadSongForm
from genreApp.utils.genre_finder import genre_finder,convert_to_wav,feature_extract
# Create your views here.

User = get_user_model()

def genreHome(request):
    if request.method == "POST":
        form = UploadSongForm(request.POST, request.FILES)
        if form.is_valid():
            song_obj = form.save(commit=False)
            song_obj.user = User.objects.get(email="admin@gmail.com")
            song_obj.name = song_obj.file.name

            song_obj.save()
            
            # Convert and Extract Features
            file_path = song_obj.file.path
            wav_path = convert_to_wav(file_path)  # Convert to WAV
            song, sr = librosa.load(wav_path, sr=None)
            features = feature_extract(song, sr)

            genre = genre_finder(features)

            # Save extracted features
            for key, value in features.items():
                setattr(song_obj, key, value)

            song_obj.genre = genre
            song_obj.duration = len(song) / 1000
            song_obj.save()  # Save to DB
            
            return render(request, "genreApp/genre-result.html", {"song": song_obj})

    else:
        form = UploadSongForm()
    return render(request,'genreApp/genre-home.html')
