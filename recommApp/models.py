from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Playlist(models.Model):
    playlistID = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Foreign Key linking to User
    songID = models.CharField(max_length=50)
    recommSongs = ArrayField(models.CharField(max_length=50), blank=True, null=True)  # List of Spotify Song IDs

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.playlistID}"