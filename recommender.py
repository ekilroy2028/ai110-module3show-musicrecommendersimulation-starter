import pandas as pd

# ----------------------------
# 1. Load the songs dataset
# ----------------------------
songs = pd.read_csv('data/songs.csv')

# ----------------------------
# 2. Define user preferences
# ----------------------------
user_preferences = {
    'genre': 'Pop',
    'mood': 'Energetic',
    'energy': 0.8,
    'tempo_bpm': 120
}

# ----------------------------
# 3. Scoring Rule (one song)
# ----------------------------
def score_song(song, prefs):
    # Categorical matching
    genre_score = 1 if song['genre'] == prefs['genre'] else 0
    mood_score  = 1 if song['mood']  == prefs['mood']  else 0

    # Numerical closeness (1 = perfect match, 0 = furthest away)
    energy_score = 1 - abs(song['energy'] - prefs['energy']) / 1.0
    tempo_score  = 1 - abs(song['tempo_bpm'] - prefs['tempo_bpm']) / 120

    # Weighted total score
    total = (0.4 * genre_score +
             0.3 * mood_score  +
             0.2 * energy_score +
             0.1 * tempo_score)

    return round(total, 4)

# ----------------------------
# 4. Ranking Rule (all songs)
# ----------------------------
songs['score'] = songs.apply(lambda row: score_song(row, user_preferences), axis=1)
ranked = songs.sort_values('score', ascending=False).reset_index(drop=True)

# ----------------------------
# 5. Display recommendations
# ----------------------------
print("\n🎵 User Preferences:")
for k, v in user_preferences.items():
    print(f"   {k}: {v}")

print("\n🏆 Top 5 Recommended Songs:")
print("-" * 55)
top5 = ranked.head(5)[['title', 'artist', 'genre', 'mood', 'score']]
for i, row in top5.iterrows():
    print(f"{i+1}. {row['title']} - {row['artist']}")
    print(f"   Genre: {row['genre']} | Mood: {row['mood']} | Score: {row['score']}")
print("-" * 55)