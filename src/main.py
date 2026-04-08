import os
import sys
from tabulate import tabulate

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
        'favorite_genre':         'Pop',
        'favorite_mood':          'Energetic',
        'target_energy':          0.8,
        'target_tempo_bpm':       120,
        'target_danceability':    0.75,
        'target_acousticness':    0.15,
        'target_detailed_mood':   'euphoric',
        'target_decade':          '2020s',
        'target_instrumentalness': 0.0,
        'prefer_studio':          True
    },
    "😌 Chill Lofi": {
        'favorite_genre':         'R&B',
        'favorite_mood':          'Mellow',
        'target_energy':          0.3,
        'target_tempo_bpm':       80,
        'target_danceability':    0.5,
        'target_acousticness':    0.7,
        'target_detailed_mood':   'romantic',
        'target_decade':          '2010s',
        'target_instrumentalness': 0.3,
        'prefer_studio':          True
    },
    "🤘 Deep Intense Rock": {
        'favorite_genre':         'Rock',
        'favorite_mood':          'Intense',
        'target_energy':          0.9,
        'target_tempo_bpm':       160,
        'target_danceability':    0.4,
        'target_acousticness':    0.1,
        'target_detailed_mood':   'aggressive',
        'target_decade':          '2000s',
        'target_instrumentalness': 0.0,
        'prefer_studio':          True
    },
    "⚡ Edge Case - High Energy but Sad": {
        'favorite_genre':         'Pop',
        'favorite_mood':          'Sad',
        'target_energy':          0.9,
        'target_tempo_bpm':       140,
        'target_danceability':    0.6,
        'target_acousticness':    0.2,
        'target_detailed_mood':   'heartbroken',
        'target_decade':          '2010s',
        'target_instrumentalness': 0.0,
        'prefer_studio':          True
    },
    "🎹 Edge Case - Classical Intensity": {
        'favorite_genre':         'Classical',
        'favorite_mood':          'Dramatic',
        'target_energy':          0.9,
        'target_tempo_bpm':       160,
        'target_danceability':    0.2,
        'target_acousticness':    0.9,
        'target_detailed_mood':   'melancholic',
        'target_decade':          '1800s',
        'target_instrumentalness': 0.9,
        'prefer_studio':          True
    }
}

# ----------------------------
# Main function
# ----------------------------
def format_table(recommendations):
    """Format recommendations as a readable table with reasons."""
    rows = []
    for i, song in enumerate(recommendations, 1):
        rows.append([
            i,
            f"{song['title']} - {song['artist']}",
            song['genre'],
            song['mood'],
            song['score'],
            "\n".join(song['reasons'])
        ])
    headers = ["#", "Song & Artist", "Genre", "Mood", "Score", "Reasons"]
    return tabulate(rows, headers=headers, tablefmt="fancy_grid")


def main():
    print(f"\n{'=' * 70}")
    print(" 🎵  VibeFinder 1.0 — Music Recommender".center(70))
    print(f"{'=' * 70}")

    songs = load_songs(SONGS_FILE)
    print(f"\n✅ Loaded {len(songs)} songs from dataset\n")

    # --- All profiles with diversity ON ---
    for profile_name, prefs in profiles.items():
        songs = load_songs(SONGS_FILE)
        recommendations = recommend(songs, prefs, top_k=5, mode='genre-first', diversity=True)

        print(f"\n{'─' * 70}")
        print(f" 👤  Profile: {profile_name}")
        print(f"     Genre: {prefs['favorite_genre']} | Mood: {prefs['favorite_mood']} | Energy: {prefs['target_energy']} | Tempo: {prefs['target_tempo_bpm']} BPM")
        print(f"{'─' * 70}")
        print(format_table(recommendations))

    # --- Diversity ON vs OFF comparison ---
    print(f"\n\n{'=' * 70}")
    print(" 🔬  DIVERSITY COMPARISON — High-Energy Pop".center(70))
    print(f"{'=' * 70}")
    test_prefs = profiles["🎵 High-Energy Pop"]

    for diversity_on in [False, True]:
        label = "✅ Diversity ON" if diversity_on else "❌ Diversity OFF"
        songs = load_songs(SONGS_FILE)
        recs = recommend(songs, test_prefs, top_k=5, mode='genre-first', diversity=diversity_on)
        rows = [[i+1, f"{s['title']} - {s['artist']}", s['genre'], s['score']]
                for i, s in enumerate(recs)]
        print(f"\n{label}")
        print(tabulate(rows, headers=["#", "Song & Artist", "Genre", "Score"], tablefmt="fancy_grid"))

    # --- Mode comparison ---
    print(f"\n\n{'=' * 70}")
    print(" 🎛️   MODE COMPARISON — High-Energy Pop".center(70))
    print(f"{'=' * 70}")
    for mode in ['genre-first', 'mood-first', 'energy-focused', 'popularity-boost']:
        songs = load_songs(SONGS_FILE)
        recs = recommend(songs, test_prefs, top_k=3, mode=mode, diversity=True)
        rows = [[i+1, f"{s['title']} - {s['artist']}", s['genre'], s['score'],
                "\n".join(s['reasons'])] for i, s in enumerate(recs)]
        print(f"\n🎛️  Mode: {mode.upper()}")
        print(tabulate(rows, headers=["#", "Song & Artist", "Genre", "Score", "Reasons"], tablefmt="fancy_grid"))

if __name__ == "__main__":
    main()