from django.conf import settings
import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
import os

model_path_E = os.path.join(settings.MEDIA_ROOT, "ML_models/knn_model.pkl")
features_path_E = os.path.join(settings.MEDIA_ROOT, "ML_models/feature_matrix.pkl")

model_path = os.path.join(settings.MEDIA_ROOT, "ML_models/knn_model.pkl")
features_path = os.path.join(settings.MEDIA_ROOT, "ML_models/feature_matrix.pkl")

def train_and_save_knn_model(merged_df):
    global model_path_E,features_path_E
    feature_cols = ["danceability", "energy", "valence", "tempo", "acousticness", "instrumentalness", "liveness", "speechiness", "loudness"]
    scaler = StandardScaler()
    feature_matrix = scaler.fit_transform(merged_df[feature_cols])
    
    nn_model = NearestNeighbors(n_neighbors=6, metric="cosine", algorithm="auto")  # 6 because the first result is the song itself
    nn_model.fit(feature_matrix)
    
    # Save model and feature matrix
    joblib.dump(nn_model, model_path_E)
    joblib.dump(feature_matrix, features_path_E)
    print("Model and features saved!")
    
    return nn_model, feature_matrix


def load_knn_model():
    global model_path,features_path
    if os.path.exists(model_path) and os.path.exists(features_path):
        nn_model = joblib.load(model_path)
        feature_matrix = joblib.load(features_path)
        print("Loaded saved model and features!")
        return nn_model, feature_matrix
    else:
        print("No saved model found, training a new one...")
        return None, None

def recommend_songs(song_name, merged_df, nn_model, feature_matrix, num_recommendations=5):
    if song_name not in merged_df["song_id"].values:
        return f"Song '{song_name}' not found."
    
    # Get the index of the song
    song_idx = merged_df[merged_df["song_id"] == song_name].index[0]
    
    # Find nearest neighbors
    distances, indices = nn_model.kneighbors([feature_matrix[song_idx]])
    
    # Get recommended songs with similarity scores
    # recommended_songs = [(merged_df.iloc[i]["song_name"], round(dist, 4)) for i, dist in zip(indices[0][1:num_recommendations+1], distances[0][1:num_recommendations+1])]
    # return recommended_songs
    recommended_songs = []
    for i, dist in zip(indices[0][1:], distances[0][1:]):  # Skip the first result (itself)
        recommended_songs.append({
            "song_name": merged_df.iloc[i]["song_name"],
            "song_id": merged_df.iloc[i]["song_id"],
            "similarity": round(1 - dist, 4)  # Convert distance to similarity
        })

    return recommended_songs