from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
import librosa
from .forms import UploadSongForm
from genreApp.utils.genre_finder import genre_finder,convert_to_wav,feature_extract
# Create your views here.

User = get_user_model()

def genreHome(request):
    current_user = request.session.get('current_user')
    print(current_user)
    
    if request.method == "POST":
        print("njadbaksjdbkasjdbajksbd")
        form = UploadSongForm(request.POST, request.FILES)
        if form.is_valid():
            song_obj = form.save(commit=False)
            song_obj.user = User.objects.get(email="admin@gmail.com")
            song_obj.name = song_obj.file.name
            print("njadbaksjdbkasjdbajksbd")
            song_obj.save()
            print("njadbaksjdbkasjdbajksbd")
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
    
    context = {
        "current_user": current_user,
        "form": form  # Add the form to the context
    }
    return render(request,'genreApp/genre-home.html', context)

def home(request):
    return render(request,'genreApp/home.html')