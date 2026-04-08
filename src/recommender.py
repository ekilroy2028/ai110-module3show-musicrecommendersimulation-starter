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
                'song_id':          int(row['song_id']),
                'title':            row['title'],
                'artist':           row['artist'],
                'genre':            row['genre'],
                'mood':             row['mood'],
                'energy':           float(row['energy']),
                'tempo_bpm':        int(row['tempo_bpm']),
                'danceability':     float(row['danceability']),
                'acousticness':     float(row['acousticness']),
                'duration_sec':     int(row['duration_sec']),
                # New advanced features
                'popularity':       int(row['popularity']),
                'release_decade':   row['release_decade'],
                'detailed_mood':    row['detailed_mood'],
                'instrumentalness': float(row['instrumentalness']),
                'liveness':         float(row['liveness']),
            })
    return songs


# ----------------------------
# Score a single song
# Returns: (numeric_score, reasons_list)
#
# Scoring Rules (max = 8.0 points):
#   Genre match:         +2.0  (exact)
#   Mood match:          +1.5  (exact)
#   Energy similarity:   up to +1.0
#   Tempo similarity:    up to +0.5
#   Detailed mood match: +1.0  (exact)
#   Popularity bonus:    up to +0.5  (higher = more points)
#   Decade match:        +0.5  (exact)
#   Instrumentalness:    up to +0.5  (similarity)
#   Liveness penalty:    up to -0.5  (high liveness = live recording = less studio polish)
# ----------------------------
def score_song(song, prefs):
    score = 0.0
    reasons = []

    # Genre match (+2.0)
    if song['genre'] == prefs['favorite_genre']:
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match (+1.5)
    if song['mood'] == prefs['favorite_mood']:
        score += 1.5
        reasons.append("mood match (+1.5)")

    # Energy similarity (up to +1.0)
    energy_sim = 1 - abs(song['energy'] - prefs['target_energy']) / 1.0
    energy_pts = round(energy_sim * 1.0, 2)
    score += energy_pts
    reasons.append(f"energy similarity (+{energy_pts})")

    # Tempo similarity (up to +0.5)
    tempo_sim = max(0, 1 - abs(song['tempo_bpm'] - prefs['target_tempo_bpm']) / 120)
    tempo_pts = round(tempo_sim * 0.5, 2)
    score += tempo_pts
    reasons.append(f"tempo similarity (+{tempo_pts})")

    # Detailed mood match (+1.0)
    if song['detailed_mood'] == prefs.get('target_detailed_mood', ''):
        score += 1.0
        reasons.append("detailed mood match (+1.0)")

    # Popularity bonus (up to +0.5)
    # Songs with popularity >= 85 get full bonus, scaled below that
    pop_pts = round(min(song['popularity'], 85) / 85 * 0.5, 2)
    score += pop_pts
    reasons.append(f"popularity bonus (+{pop_pts})")

    # Release decade match (+0.5)
    if song['release_decade'] == prefs.get('target_decade', ''):
        score += 0.5
        reasons.append("decade match (+0.5)")

    # Instrumentalness similarity (up to +0.5)
    inst_sim = 1 - abs(song['instrumentalness'] - prefs.get('target_instrumentalness', 0.0))
    inst_pts = round(inst_sim * 0.5, 2)
    score += inst_pts
    reasons.append(f"instrumentalness match (+{inst_pts})")

    # Liveness penalty (up to -0.5)
    # High liveness means it's a live recording — penalize if user wants studio sound
    if prefs.get('prefer_studio', True):
        liveness_penalty = round(song['liveness'] * 0.5, 2)
        score -= liveness_penalty
        if liveness_penalty > 0.1:
            reasons.append(f"liveness penalty (-{liveness_penalty})")

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