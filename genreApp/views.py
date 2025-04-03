from django.shortcuts import render
from django.contrib.auth import get_user_model
import librosa
from .forms import UploadSongForm
from genreApp.utils.genre_finder import genre_finder, convert_to_wav, feature_extract

User = get_user_model()

def genreHome(request):
    current_user = request.session.get('current_user')
    form = UploadSongForm()
    context = {
        "current_user": current_user,
        "form": form,
        "analysis_complete": False
    }
    
    if request.method == "POST":
        form = UploadSongForm(request.POST, request.FILES)
        if form.is_valid():
            song_obj = form.save(commit=False)
            song_obj.user = User.objects.get(email="admin@gmail.com")
            song_obj.name = song_obj.file.name.split('/')[-1]  # Get just the filename without path
            
            # Clean the filename for display
            if '\\' in song_obj.name:
                song_obj.name = song_obj.name.split('\\')[-1]
                
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
            song_obj.duration = len(song) / sr  # Duration in seconds
            song_obj.save()
            
            # Add song and success flag to context
            context["song"] = song_obj
            context["analysis_complete"] = True
            context["form"] = UploadSongForm()  # Reset form for new upload
    
    return render(request, 'genreApp/genre-home.html', context)

def home(request):
    return render(request, 'genreApp/home.html')