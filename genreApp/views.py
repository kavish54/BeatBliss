import os
import pickle
from django.conf import settings
from django.shortcuts import render
from django.contrib.auth import get_user_model
import librosa
from .forms import UploadSongForm
from genreApp.utils.genre_finder import convert_to_wav,extract_features,predict_genre

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
            MODEL_SAVE_PATH = os.path.join(settings.BASE_DIR, "media", "ML_models", "genre_classifier_model.pkl")
            file_path = song_obj.file.path
            with open(MODEL_SAVE_PATH, 'rb') as f:
                loaded_model = pickle.load(f)
            result = predict_genre(loaded_model, file_path)

            
            # Add song and success flag to context
            genres = []
            perc = []
            for pred in result['predictions']:
                # Convert probability to percentage
                genres.append(str(pred['genre']).upper())
                perc.append(round(pred['probability'] * 100, 2))
            context["genres"] = genres
            context["perc"] = perc
            context["song"] = song_obj
            context["analysis_complete"] = True
            context["form"] = UploadSongForm()  # Reset form for new upload
    
    return render(request, 'genreApp/genre-home.html', context)

def home(request):
    return render(request, 'genreApp/home.html')


def aboutus(request):
    return render(request, 'genreApp/aboutus.html')