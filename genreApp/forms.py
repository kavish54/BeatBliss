from django import forms
from .models import Song

class UploadSongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['file']
        widgets = {
            'file': forms.ClearableFileInput(attrs={'id': 'file-upload'}),
        }