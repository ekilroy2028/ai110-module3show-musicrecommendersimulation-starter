import pandas as pd

# ----------------------------
# 1. Load the songs dataset
# ----------------------------
songs = pd.read_csv('data/songs.csv')

# ----------------------------
# 2. Define user preferences
# ----------------------------
user_preferences = {
    'favorite_genre': 'Pop',
    'favorite_mood': 'Energetic',
    'target_energy': 0.8,
    'target_tempo_bpm': 120,
    'target_danceability': 0.75,
    'target_acousticness': 0.15
}

# ----------------------------
# 3. Scoring Rule (one song)
# Algorithm Recipe:
#   +2.0 points for genre match
#   +1.5 points for mood match
#   +1.0 point for energy similarity (scaled 0.0–1.0)
#   +0.5 points for tempo similarity (scaled 0.0–1.0)
#   Max possible score = 5.0
# ----------------------------
def score_song(song, prefs):
    score = 0.0

    # Categorical matching
    if song['genre'] == prefs['favorite_genre']:
        score += 2.0

    if song['mood'] == prefs['favorite_mood']:
        score += 1.5

    # Energy similarity (0.0–1.0 scale, worth up to 1.0 point)
    energy_similarity = 1 - abs(song['energy'] - prefs['target_energy']) / 1.0
    score += energy_similarity * 1.0

    # Tempo similarity (60–180 BPM range = 120 spread, worth up to 0.5 points)
    tempo_similarity = 1 - abs(song['tempo_bpm'] - prefs['target_tempo_bpm']) / 120
    tempo_similarity = max(0, tempo_similarity)  # clamp to 0 minimum
    score += tempo_similarity * 0.5

    return round(score, 4)

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

print(f"\n   Max possible score: 5.0")
print("\n🏆 Top 5 Recommended Songs:")
print("-" * 60)
top5 = ranked.head(5)[['title', 'artist', 'genre', 'mood', 'score']]
for i, row in top5.iterrows():
    print(f"{i+1}. {row['title']} - {row['artist']}")
    print(f"   Genre: {row['genre']} | Mood: {row['mood']} | Score: {row['score']} / 5.0")
print("-" * 60)