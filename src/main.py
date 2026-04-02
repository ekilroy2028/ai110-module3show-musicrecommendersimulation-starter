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
# Multiple User Profiles
# ----------------------------
profiles = {
    "🎵 High-Energy Pop": {
        'favorite_genre':      'Pop',
        'favorite_mood':       'Energetic',
        'target_energy':       0.8,
        'target_tempo_bpm':    120,
        'target_danceability': 0.75,
        'target_acousticness': 0.15
    },
    "😌 Chill Lofi": {
        'favorite_genre':      'R&B',
        'favorite_mood':       'Mellow',
        'target_energy':       0.3,
        'target_tempo_bpm':    80,
        'target_danceability': 0.5,
        'target_acousticness': 0.7
    },
    "🤘 Deep Intense Rock": {
        'favorite_genre':      'Rock',
        'favorite_mood':       'Intense',
        'target_energy':       0.9,
        'target_tempo_bpm':    160,
        'target_danceability': 0.4,
        'target_acousticness': 0.1
    },
    "⚡ Edge Case - High Energy but Sad": {
        'favorite_genre':      'Pop',
        'favorite_mood':       'Sad',
        'target_energy':       0.9,
        'target_tempo_bpm':    140,
        'target_danceability': 0.6,
        'target_acousticness': 0.2
    },
    "🎹 Edge Case - Classical Intensity": {
        'favorite_genre':      'Classical',
        'favorite_mood':       'Dramatic',
        'target_energy':       0.9,
        'target_tempo_bpm':    160,
        'target_danceability': 0.2,
        'target_acousticness': 0.9
    }
}

# ----------------------------
# Main function
# ----------------------------
def main():
    songs = load_songs(SONGS_FILE)
    print(f"Loaded songs: {len(songs)}\n")
    print("=" * 60)

    for profile_name, prefs in profiles.items():
        # Reload songs each time to reset scores
        songs = load_songs(SONGS_FILE)
        recommendations = recommend(songs, prefs, top_k=5)

        print(f"\n👤 Profile: {profile_name}")
        print(f"   Genre: {prefs['favorite_genre']} | Mood: {prefs['favorite_mood']} | Energy: {prefs['target_energy']} | Tempo: {prefs['target_tempo_bpm']} BPM")
        print(f"\n🏆 Top 5 Recommendations:")
        print("-" * 60)
        for i, song in enumerate(recommendations, 1):
            print(f"{i}. {song['title']} - {song['artist']}")
            print(f"   Genre: {song['genre']} | Mood: {song['mood']} | Score: {song['score']} / 5.0")
            print(f"   Why: {' | '.join(song['reasons'])}")
        print("=" * 60)

if __name__ == "__main__":
    main()