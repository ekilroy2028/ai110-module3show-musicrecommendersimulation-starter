import os
import sys

# Make sure src/ can find recommender.py
sys.path.insert(0, os.path.dirname(__file__))

from recommender import load_songs, recommend

# ----------------------------
# File path to songs dataset
# ----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SONGS_FILE = os.path.join(BASE_DIR, 'data', 'songs.csv')

# ----------------------------
# User preferences
# ----------------------------
user_preferences = {
    'favorite_genre':      'Pop',
    'favorite_mood':       'Energetic',
    'target_energy':       0.8,
    'target_tempo_bpm':    120,
    'target_danceability': 0.75,
    'target_acousticness': 0.15
}

# ----------------------------
# Main function
# ----------------------------
def main():
    songs = load_songs(SONGS_FILE)
    print(f"Loaded songs: {len(songs)}")

    recommendations = recommend(songs, user_preferences, top_k=5)

    print(f"\n🎵 User Preferences:")
    for k, v in user_preferences.items():
        print(f"   {k}: {v}")

    print(f"\n🏆 Top 5 Recommended Songs:")
    print("-" * 60)
    for i, song in enumerate(recommendations, 1):
        print(f"{i}. {song['title']} - {song['artist']}")
        print(f"   Genre: {song['genre']} | Mood: {song['mood']} | Score: {song['score']} / 5.0")
        print(f"   Why: {' | '.join(song['reasons'])}")
    print("-" * 60)

if __name__ == "__main__":
    main()