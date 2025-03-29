from django.conf import settings
from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    liked_playlist = ArrayField(
        models.IntegerField(),  # Store Playlist IDs (AutoField in Playlist model)
        blank=True,
        default=list
    )
    liked_song_list = ArrayField(
        models.CharField(max_length=100),  # Spotify Song IDs
        blank=True,
        default=list
    )

    def __str__(self):
        return f"{self.user.email}'s Profile"