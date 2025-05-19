from django.conf import settings
import joblib
import librosa
import numpy as np
import os
import pandas as pd
from pydub import AudioSegment
from sklearn import preprocessing

def convert_to_wav(file_path):
    
    # Converts an audio file (MP3, etc.) to WAV and replaces the original file.
    
    file_root, ext = os.path.splitext(file_path)
    wav_path = file_root + ".wav"  # Replace extension with .wav

    if ext.lower() != ".wav":
        audio = AudioSegment.from_file(file_path, format=ext[1:])  # Convert from existing format
        audio.export(wav_path, format="wav")  # Save as WAV
        os.remove(file_path)  # Delete old file

    return wav_path

# Feature extraction function
def extract_features(file_path, duration=30):
    try:
        # Load audio file with a fixed duration
        y, sr = librosa.load(file_path, mono=True, duration=duration)
        
        # Feature set 1: Spectral features
        chroma_stft = librosa.feature.chroma_stft(y=y, sr=sr)
        spec_cent = librosa.feature.spectral_centroid(y=y, sr=sr)
        spec_bw = librosa.feature.spectral_bandwidth(y=y, sr=sr)
        rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y)
        
        # Feature set 2: Rhythm features
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        
        # Feature set 3: MFCC (crucial for genre classification)
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
        
        # Feature set 4: Energy and RMS
        rms = librosa.feature.rms(y=y)
        
        # Feature set 5: Harmonic and Percussive components
        harmonic, percussive = librosa.effects.hpss(y)
        harmonic_mean = np.mean(harmonic)
        percussive_mean = np.mean(percussive)
        
        # Aggregate all features using statistical measures
        features = {
            'chroma_stft_mean': np.mean(chroma_stft),
            'chroma_stft_var': np.var(chroma_stft),
            'spec_cent_mean': np.mean(spec_cent),
            'spec_cent_var': np.var(spec_cent),
            'spec_bw_mean': np.mean(spec_bw),
            'spec_bw_var': np.var(spec_bw),
            'rolloff_mean': np.mean(rolloff),
            'rolloff_var': np.var(rolloff),
            'zcr_mean': np.mean(zcr),
            'zcr_var': np.var(zcr),
            'tempo': tempo,
            'harmonic_mean': harmonic_mean,
            'percussive_mean': percussive_mean,
            'rms_mean': np.mean(rms),
            'rms_var': np.var(rms),
        }
        
        # Add MFCC features
        for i in range(20):
            features[f'mfcc{i+1}_mean'] = np.mean(mfcc[i])
            features[f'mfcc{i+1}_var'] = np.var(mfcc[i])
        
        return features
    
    except Exception as e:
        print(f"Error extracting features from {file_path}: {e}")
        return None

# Function to predict genre for a new song
def predict_genre(model_data, file_path):
    try:
        # Extract model and label encoder
        model = model_data['model'] if isinstance(model_data, dict) else model_data
        label_encoder = model_data.get('label_encoder') if isinstance(model_data, dict) else None
        
        # Check if file is MP3 and convert to WAV if needed
        if file_path.lower().endswith('.mp3'):
            print("Converting MP3 to WAV for processing...")
            temp_wav = file_path.replace('.mp3', '_temp.wav')
            try:
                audio = AudioSegment.from_mp3(file_path)
                audio.export(temp_wav, format="wav")
                file_path = temp_wav
                print(f"Converted to temporary file: {temp_wav}")
            except Exception as e:
                print(f"Error converting MP3 to WAV: {e}")
                return {
                    "top_genre": "unknown",
                    "predictions": [{"genre": "unknown", "probability": 0.0}],
                    "error": f"MP3 conversion failed: {str(e)}"
                }
        
        # Extract features from the new song
        features = extract_features(file_path)
        
        if not features:
            return {
                "top_genre": "unknown",
                "predictions": [{"genre": "unknown", "probability": 0.0}],
                "error": "Could not extract features from the file."
            }
        
        # Convert to DataFrame with the same structure as training data
        features_df = pd.DataFrame([features])
        
        # Ensure feature columns match what the model expects
        if hasattr(model, 'feature_names_in_'):
            expected_features = model.feature_names_in_
        elif hasattr(model, 'steps') and hasattr(model.steps[-1][1], 'feature_names_in_'):
            expected_features = model.steps[-1][1].feature_names_in_
        else:
            # If we can't determine expected features, use what we have
            expected_features = features_df.columns
            
        # Create a DataFrame with expected columns
        aligned_features = pd.DataFrame(0, index=[0], columns=expected_features)
        
        # Fill in values for columns we have
        for col in features_df.columns:
            if col in expected_features:
                aligned_features[col] = features_df[col]
        
        # Make prediction using the classifier directly to avoid pipeline issues
        if hasattr(model, 'steps') and len(model.steps) > 0:
            # For pipeline, apply each step manually
            X = aligned_features
            for name, transform in model.steps[:-1]:
                X = transform.transform(X)
            prediction = model.steps[-1][1].predict(X)
            probabilities = model.steps[-1][1].predict_proba(X)[0]
            classes = model.steps[-1][1].classes_
        else:
            # For single model
            prediction = model.predict(aligned_features)
            probabilities = model.predict_proba(aligned_features)[0]
            classes = model.classes_
        
        # Convert numeric prediction back to genre name if label encoder is available
        if label_encoder is not None:
            genre_prediction = label_encoder.inverse_transform(prediction)[0]
        else:
            genre_prediction = prediction[0]
        
        # Create a dictionary of genre:probability pairs
        if label_encoder is not None:
            genre_probs = {label_encoder.inverse_transform([cls])[0]: prob for cls, prob in zip(classes, probabilities)}
        else:
            genre_probs = {cls: prob for cls, prob in zip(classes, probabilities)}
        
        # Sort by probability (descending)
        sorted_genres = sorted(genre_probs.items(), key=lambda x: x[1], reverse=True)
        
        # Return top 3 predictions with probabilities
        top_predictions = [
            {"genre": genre, "probability": float(prob)} 
            for genre, prob in sorted_genres[:3]
        ]
        
        # Clean up temporary file if created
        if file_path.endswith('_temp.wav') and os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Removed temporary file: {file_path}")
            except:
                pass
        
        return {
            "top_genre": genre_prediction,
            "predictions": top_predictions
        }
        
    except Exception as e:
        print(f"Error predicting genre: {e}")
        print("This could be due to a mismatch between the features used for training and prediction.")
        print("Try retraining the model or using a different model.")
        return {
            "top_genre": "unknown",
            "predictions": [{"genre": "unknown", "probability": 0.0}],
            "error": str(e)
        }