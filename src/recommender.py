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
                'popularity':       int(row['popularity']),
                'release_decade':   row['release_decade'],
                'detailed_mood':    row['detailed_mood'],
                'instrumentalness': float(row['instrumentalness']),
                'liveness':         float(row['liveness']),
            })
    return songs


# ============================================================
# SCORING STRATEGIES
# Each strategy is a function that takes (song, prefs)
# and returns (score, reasons). Easy to add new ones!
# ============================================================

def genre_first_score(song, prefs):
    """Strategy 1: Genre-First — heavily rewards genre matches."""
    score = 0.0
    reasons = []

    # Genre is king — worth 3.0
    if song['genre'] == prefs['favorite_genre']:
        score += 3.0
        reasons.append("genre match (+3.0)")

    if song['mood'] == prefs['favorite_mood']:
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_pts = round((1 - abs(song['energy'] - prefs['target_energy'])) * 0.5, 2)
    score += energy_pts
    reasons.append(f"energy similarity (+{energy_pts})")

    tempo_sim = max(0, 1 - abs(song['tempo_bpm'] - prefs['target_tempo_bpm']) / 120)
    tempo_pts = round(tempo_sim * 0.5, 2)
    score += tempo_pts
    reasons.append(f"tempo similarity (+{tempo_pts})")

    return round(score, 4), reasons


def mood_first_score(song, prefs):
    """Strategy 2: Mood-First — prioritizes emotional vibe over genre."""
    score = 0.0
    reasons = []

    if song['mood'] == prefs['favorite_mood']:
        score += 3.0
        reasons.append("mood match (+3.0)")

    if song['detailed_mood'] == prefs.get('target_detailed_mood', ''):
        score += 1.0
        reasons.append("detailed mood match (+1.0)")

    if song['genre'] == prefs['favorite_genre']:
        score += 0.5
        reasons.append("genre match (+0.5)")

    energy_pts = round((1 - abs(song['energy'] - prefs['target_energy'])) * 0.5, 2)
    score += energy_pts
    reasons.append(f"energy similarity (+{energy_pts})")

    return round(score, 4), reasons


def energy_focused_score(song, prefs):
    """Strategy 3: Energy-Focused — numeric features dominate."""
    score = 0.0
    reasons = []

    # Energy is worth the most
    energy_pts = round((1 - abs(song['energy'] - prefs['target_energy'])) * 3.0, 2)
    score += energy_pts
    reasons.append(f"energy similarity (+{energy_pts})")

    tempo_sim = max(0, 1 - abs(song['tempo_bpm'] - prefs['target_tempo_bpm']) / 120)
    tempo_pts = round(tempo_sim * 1.5, 2)
    score += tempo_pts
    reasons.append(f"tempo similarity (+{tempo_pts})")

    dance_pts = round((1 - abs(song['danceability'] - prefs.get('target_danceability', 0.5))) * 0.5, 2)
    score += dance_pts
    reasons.append(f"danceability similarity (+{dance_pts})")

    if song['genre'] == prefs['favorite_genre']:
        score += 0.5
        reasons.append("genre match (+0.5)")

    return round(score, 4), reasons


def popularity_boost_score(song, prefs):
    """Strategy 4: Popularity-Boost — favors well-known, highly rated songs."""
    score = 0.0
    reasons = []

    # Popularity is the main driver
    pop_pts = round(song['popularity'] / 100 * 3.0, 2)
    score += pop_pts
    reasons.append(f"popularity score (+{pop_pts})")

    if song['genre'] == prefs['favorite_genre']:
        score += 1.0
        reasons.append("genre match (+1.0)")

    if song['mood'] == prefs['favorite_mood']:
        score += 1.0
        reasons.append("mood match (+1.0)")

    return round(score, 4), reasons


# ============================================================
# STRATEGY REGISTRY
# Maps mode name → scoring function
# To add a new mode, just add it here!
# ============================================================
SCORING_MODES = {
    'genre-first':       genre_first_score,
    'mood-first':        mood_first_score,
    'energy-focused':    energy_focused_score,
    'popularity-boost':  popularity_boost_score,
}


# ----------------------------
# Diversity Penalty
# Penalizes songs if their artist or genre
# is already in the selected results list.
#
# Penalty rules:
#   -0.5 if artist already appears in results
#   -0.3 if genre already appears 2+ times in results
# ----------------------------
def apply_diversity_penalty(song, selected):
    penalty = 0.0
    reasons = []

    selected_artists = [s['artist'] for s in selected]
    selected_genres  = [s['genre']  for s in selected]

    if song['artist'] in selected_artists:
        penalty += 0.5
        reasons.append("repeat artist (-0.5)")

    if selected_genres.count(song['genre']) >= 2:
        penalty += 0.3
        reasons.append("genre overrepresented (-0.3)")

    return penalty, reasons


# ----------------------------
# Rank all songs
# ----------------------------
def recommend(songs, prefs, top_k=5, mode='genre-first', diversity=True):
    if mode not in SCORING_MODES:
        raise ValueError(f"Unknown mode '{mode}'. Choose from: {list(SCORING_MODES.keys())}")

    strategy = SCORING_MODES[mode]

    # Step 1 — Score every song
    scored = []
    for song in songs:
        score, reasons = strategy(song, prefs)
        song['score']        = score
        song['base_score']   = score
        song['reasons']      = reasons[:]
        scored.append(song)

    # Step 2 — Sort by base score
    scored = sorted(scored, key=lambda x: x['score'], reverse=True)

    if not diversity:
        return scored[:top_k]

    # Step 3 — Greedily build results with diversity penalties
    selected = []
    candidates = scored[:]

    while len(selected) < top_k and candidates:
        # Re-apply diversity penalty to all remaining candidates
        for song in candidates:
            penalty, pen_reasons = apply_diversity_penalty(song, selected)
            song['score'] = round(song['base_score'] - penalty, 4)
            # Show penalty in reasons if not already there
            song['reasons'] = song['reasons'][:] 
            for r in pen_reasons:
                if r not in song['reasons']:
                    song['reasons'].append(r)

        # Pick the highest scoring candidate after penalties
        candidates.sort(key=lambda x: x['score'], reverse=True)
        selected.append(candidates.pop(0))

    return selected