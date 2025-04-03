from django import forms
from .models import Song

class UploadSongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={
                'id': 'file-upload',
                'accept': 'audio/*',
                'onchange': 'displayFileName(this)'
            }),
        }