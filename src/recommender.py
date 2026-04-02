import csv
import os

# ----------------------------
# Load songs from CSV file
# ----------------------------
def load_songs(filepath):
    songs = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            songs.append({
                'song_id':      int(row['song_id']),
                'title':        row['title'],
                'artist':       row['artist'],
                'genre':        row['genre'],
                'mood':         row['mood'],
                'energy':       float(row['energy']),
                'tempo_bpm':    int(row['tempo_bpm']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness']),
                'duration_sec': int(row['duration_sec'])
            })
    return songs


# ----------------------------
# Score a single song
# Returns: (numeric_score, reasons_list)
# ----------------------------
def score_song(song, prefs):
    score = 0.0
    reasons = []

    # Genre match (+2.0)
    if song['genre'] == prefs['favorite_genre']:
        score += 2.0
        reasons.append(f"genre match (+2.0)")

    # Mood match (+1.5)
    if song['mood'] == prefs['favorite_mood']:
        score += 1.5
        reasons.append(f"mood match (+1.5)")

    # Energy similarity (up to +1.0)
    energy_similarity = 1 - abs(song['energy'] - prefs['target_energy']) / 1.0
    energy_points = round(energy_similarity * 1.0, 2)
    score += energy_points
    reasons.append(f"energy similarity (+{energy_points})")

    # Tempo similarity (up to +0.5)
    tempo_similarity = 1 - abs(song['tempo_bpm'] - prefs['target_tempo_bpm']) / 120
    tempo_similarity = max(0, tempo_similarity)
    tempo_points = round(tempo_similarity * 0.5, 2)
    score += tempo_points
    reasons.append(f"tempo similarity (+{tempo_points})")

    return round(score, 4), reasons


# ----------------------------
# Rank all songs
# ----------------------------
def recommend(songs, prefs, top_k=5):
    scored = []
    for song in songs:
        score, reasons = score_song(song, prefs)
        song['score'] = score
        song['reasons'] = reasons
        scored.append(song)
    ranked = sorted(scored, key=lambda x: x['score'], reverse=True)
    return ranked[:top_k]