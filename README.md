# 🎵 BeatBliss - Music Genre Classification & Recommender System

BeatBliss is a web-based application that allows users to **upload music files**, detect their **genre** using machine learning, and receive ** recommendations** through based on their favorite songs. Designed for music lovers, curators, and enthusiasts, it bridges the gap between user preferences and music discovery.

---

## 📌 Features

- 🎶 **Genre Classification** — Supports 10 genres: Blues, Classical, Country, Disco, Hip-hop, Jazz, Reggae, Rock, Metal, Pop.
- 📁 **File Upload** — Accepts `.mp3`, `.ogg`, `.wav`, and more, with automatic `.wav` conversion.
- 🤖 **ML Models Used** — KNN (Recommendation), XGBoost (Classification)
- 📊 **Feature Extraction** — Utilizes MFCCs, chroma, spectral centroid, zero-crossing rate (via LibROSA).
- 🎧 **Spotify Integration** — Fetches track metadata 
- 🌐 **User-Friendly Interface** — Intuitive frontend for uploading, classifying, and viewing recommendations.

---

## 🛠️ Tech Stack

### Frontend
- HTML5 / CSS3 / JavaScript

### Backend
- Python
- Django

### Database
- PostgreSQL

### Libraries & APIs
- `librosa` – audio feature extraction
- `pydub` – audio conversion
- `scikit-learn`, `xgboost` – ML modeling
- `Spotify Web API` – song metadata
- `GTZAN Dataset` – training data

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9-3.12
- FFmpeg framework
- Spotify Developer Account (for API key)
- Dataset - [GTZAN Dataset - Music Genre Classification](https://www.kaggle.com/datasets/andradaolteanu/gtzan-dataset-music-genre-classification)

### Installation

```bash
git clone https://github.com/kavish54/BeatBliss.git
cd BeatBliss
```

### Environment Setup
```bash
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
```
### To Run the project
```bash
python manage.py runserver
```
## 👨‍💻 Authors
- [Priyanshi Bharakhada](https://www.linkedin.com/in/priyanshi-bharakhada/)
- [Kavish Bhavsar](https://www.linkedin.com/in/kavish-bhavsar-97b22b26a/)
- [Krishna Lalwani](https://www.linkedin.com/in/krishna-lalwani-291379253/)
- [Mihir Patel](https://www.linkedin.com/in/mihirpateldt/)

GLS University | Academic Year 2024–2025
