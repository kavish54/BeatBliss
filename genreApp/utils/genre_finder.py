from django.conf import settings
import joblib
import librosa
import numpy as np
import os
import pandas as pd
from pydub import AudioSegment
from sklearn import preprocessing

def convert_to_wav(file_path):
    """
    Converts an audio file (MP3, etc.) to WAV and replaces the original file.
    """
    file_root, ext = os.path.splitext(file_path)
    wav_path = file_root + ".wav"  # Replace extension with .wav

    if ext.lower() != ".wav":
        audio = AudioSegment.from_file(file_path, format=ext[1:])  # Convert from existing format
        audio.export(wav_path, format="wav")  # Save as WAV
        os.remove(file_path)  # Delete old file

    return wav_path

def feature_extract(song, sr):
    # Chroma STFT
    chroma_stft = librosa.feature.chroma_stft(y=song, sr=sr)
    chroma_stft_mean = np.mean(chroma_stft)
    chroma_stft_var = np.var(chroma_stft)

    # RMS Energy
    rms = librosa.feature.rms(y=song)
    rms_mean = np.mean(rms)
    rms_var = np.var(rms)

    # Spectral Features
    spectral_centroid = librosa.feature.spectral_centroid(y=song, sr=sr)
    spectral_centroid_mean = np.mean(spectral_centroid)
    spectral_centroid_var = np.var(spectral_centroid)

    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=song, sr=sr)
    spectral_bandwidth_mean = np.mean(spectral_bandwidth)
    spectral_bandwidth_var = np.var(spectral_bandwidth)

    rolloff = librosa.feature.spectral_rolloff(y=song, sr=sr)
    rolloff_mean = np.mean(rolloff)
    rolloff_var = np.var(rolloff)

    zero_crossing_rate = librosa.feature.zero_crossing_rate(y=song)
    zero_cross_mean = np.mean(zero_crossing_rate)
    zero_cross_var = np.var(zero_crossing_rate)

    # Harmony & Perceived Harmonic Content
    harmony, perceptr = librosa.effects.hpss(song)
    harmony_mean = np.mean(harmony)
    harmony_var = np.var(harmony)
    perceptr_mean = np.mean(perceptr)
    perceptr_var = np.var(perceptr)

    # Tempo
    tempo, _ = librosa.beat.beat_track(y=song, sr=sr)

    # MFCCs (Mel-frequency cepstral coefficients)
    mfccs = librosa.feature.mfcc(y=song, sr=sr, n_mfcc=20)
    mfcc_means = np.mean(mfccs, axis=1)
    mfcc_vars = np.var(mfccs, axis=1)

    # Creating the final feature dictionary
    features = {
        "chroma_stft_mean": chroma_stft_mean,
        "chroma_stft_var": chroma_stft_var,
        "rms_mean": rms_mean,
        "rms_var": rms_var,
        "spectral_centroid_mean": spectral_centroid_mean,
        "spectral_centroid_var": spectral_centroid_var,
        "spectral_bandwidth_mean": spectral_bandwidth_mean,
        "spectral_bandwidth_var": spectral_bandwidth_var,
        "rolloff_mean": rolloff_mean,
        "rolloff_var": rolloff_var,
        "zero_crossing_rate_mean": zero_cross_mean,
        "zero_crossing_rate_var": zero_cross_var,
        "harmony_mean": harmony_mean,
        "harmony_var": harmony_var,
        "perceptr_mean": perceptr_mean,
        "perceptr_var": perceptr_var,
        "tempo": tempo
    }

    # Adding MFCCs dynamically
    for i in range(20):
        features[f"mfcc{i+1}_mean"] = mfcc_means[i]
        features[f"mfcc{i+1}_var"] = mfcc_vars[i]

    return features

def genre_finder(features):
    data_path = os.path.join(settings.MEDIA_ROOT, "datasets/features.csv")
    data = pd.read_csv(data_path)
    data = data.iloc[0:,1:]
    y = data['label']
    x = data.loc[:,data.columns != 'label']

    x_max = x.max()
    x_min = x.min()
    cols = x.columns
    
    fr = pd.DataFrame(features)
    fr['length'] = 0
    fr = (fr - x_min)/(x_max - x_min)
    fr.columns = cols

    label_encoder = preprocessing.LabelEncoder()
    y = label_encoder.fit_transform(y)

    model_path = os.path.join(settings.BASE_DIR, "media", "ML_models", "xgboost_model.pkl")
    model = joblib.load(model_path)
    preds = model.predict(fr)
    genre = label_encoder.inverse_transform(preds)
    return genre
