from django.db import models
from django.conf import settings

# Create your models here.

class Song(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Track which user uploaded the song
    name = models.CharField(max_length=255)  # Song name
    duration = models.FloatField(null=True,blank=True)  # Duration in seconds
    file = models.FileField(upload_to='songs/')  # Uploaded file (stored in media/songs/)
    genre = models.CharField(max_length=100, null=True, blank=True)  # Predicted genre

    # Chroma Features
    chroma_stft_mean = models.FloatField(null=True, blank=True)
    chroma_stft_var = models.FloatField(null=True, blank=True)

    # RMS Energy
    rms_mean = models.FloatField(null=True, blank=True)
    rms_var = models.FloatField(null=True, blank=True)

    # Spectral Features
    spectral_centroid_mean = models.FloatField(null=True, blank=True)
    spectral_centroid_var = models.FloatField(null=True, blank=True)
    spectral_bandwidth_mean = models.FloatField(null=True, blank=True)
    spectral_bandwidth_var = models.FloatField(null=True, blank=True)
    rolloff_mean = models.FloatField(null=True, blank=True)
    rolloff_var = models.FloatField(null=True, blank=True)
    zero_crossing_rate_mean = models.FloatField(null=True, blank=True)
    zero_crossing_rate_var = models.FloatField(null=True, blank=True)

    # Harmonic & Perceived Features
    harmony_mean = models.FloatField(null=True, blank=True)
    harmony_var = models.FloatField(null=True, blank=True)
    perceptr_mean = models.FloatField(null=True, blank=True)
    perceptr_var = models.FloatField(null=True, blank=True)

    # Tempo
    tempo = models.FloatField(null=True, blank=True)

    # MFCCs (Mel-frequency cepstral coefficients)
    mfcc1_mean = models.FloatField(null=True, blank=True)
    mfcc1_var = models.FloatField(null=True, blank=True)
    mfcc2_mean = models.FloatField(null=True, blank=True)
    mfcc2_var = models.FloatField(null=True, blank=True)
    mfcc3_mean = models.FloatField(null=True, blank=True)
    mfcc3_var = models.FloatField(null=True, blank=True)
    mfcc4_mean = models.FloatField(null=True, blank=True)
    mfcc4_var = models.FloatField(null=True, blank=True)
    mfcc5_mean = models.FloatField(null=True, blank=True)
    mfcc5_var = models.FloatField(null=True, blank=True)
    mfcc6_mean = models.FloatField(null=True, blank=True)
    mfcc6_var = models.FloatField(null=True, blank=True)
    mfcc7_mean = models.FloatField(null=True, blank=True)
    mfcc7_var = models.FloatField(null=True, blank=True)
    mfcc8_mean = models.FloatField(null=True, blank=True)
    mfcc8_var = models.FloatField(null=True, blank=True)
    mfcc9_mean = models.FloatField(null=True, blank=True)
    mfcc9_var = models.FloatField(null=True, blank=True)
    mfcc10_mean = models.FloatField(null=True, blank=True)
    mfcc10_var = models.FloatField(null=True, blank=True)
    mfcc11_mean = models.FloatField(null=True, blank=True)
    mfcc11_var = models.FloatField(null=True, blank=True)
    mfcc12_mean = models.FloatField(null=True, blank=True)
    mfcc12_var = models.FloatField(null=True, blank=True)
    mfcc13_mean = models.FloatField(null=True, blank=True)
    mfcc13_var = models.FloatField(null=True, blank=True)
    mfcc14_mean = models.FloatField(null=True, blank=True)
    mfcc14_var = models.FloatField(null=True, blank=True)
    mfcc15_mean = models.FloatField(null=True, blank=True)
    mfcc15_var = models.FloatField(null=True, blank=True)
    mfcc16_mean = models.FloatField(null=True, blank=True)
    mfcc16_var = models.FloatField(null=True, blank=True)
    mfcc17_mean = models.FloatField(null=True, blank=True)
    mfcc17_var = models.FloatField(null=True, blank=True)
    mfcc18_mean = models.FloatField(null=True, blank=True)
    mfcc18_var = models.FloatField(null=True, blank=True)
    mfcc19_mean = models.FloatField(null=True, blank=True)
    mfcc19_var = models.FloatField(null=True, blank=True)
    mfcc20_mean = models.FloatField(null=True, blank=True)
    mfcc20_var = models.FloatField(null=True, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)  # Track when the song was uploaded

    def __str__(self):
        return self.name
