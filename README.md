# AI110 Module 3 – Music Recommender Simulation

## Project Overview
A small content-based music recommender system built in Python. It scores and ranks songs against a user's preferences using weighted rules across genre, mood, energy, and tempo.

---

## How The System Works

Real-world recommendation systems like Spotify or YouTube analyze massive amounts of user behavior and song attributes to predict what a listener will enjoy next. They combine **collaborative filtering** (finding patterns across millions of users with similar taste) with **content-based filtering** (matching the audio features of songs a user already loves). At scale, these systems use deep learning models trained on billions of data points — including skips, replays, playlist adds, time of day, and even device type — to continuously refine their predictions.

My version prioritizes **content-based filtering**. It takes a user's stated preferences (genre, mood, energy level, and tempo) and scores every song in the dataset using a weighted formula. Genre is weighted most heavily (40%) because it is the strongest broad indicator of taste, followed by mood (30%) which captures the listening vibe, then energy (20%) and tempo (10%) which fine-tune the numeric closeness of the match. Songs are then ranked by their total score and the top results are returned as recommendations.

---

## Features Used

### 🎵 Song Object Attributes
| Feature | Type | Description |
|---|---|---|
| `song_id` | Integer | Unique identifier |
| `title` | String | Song name |
| `artist` | String | Artist name |
| `genre` | Categorical | Musical genre (Pop, Rock, Hip-Hop, etc.) |
| `mood` | Categorical | Emotional tone (Happy, Sad, Energetic, etc.) |
| `energy` | Float (0–1) | Intensity and activity level |
| `tempo_bpm` | Integer | Beats per minute |
| `danceability` | Float (0–1) | How suitable the track is for dancing |
| `acousticness` | Float (0–1) | Acoustic vs. electronic quality |
| `duration_sec` | Integer | Song length in seconds |

### 👤 UserProfile Object Attributes
| Feature | Type | Description |
|---|---|---|
| `genre` | Categorical | Preferred genre |
| `mood` | Categorical | Desired mood/vibe |
| `energy` | Float (0–1) | Preferred energy level |
| `tempo_bpm` | Integer | Preferred tempo |

---

## Scoring Formula
```
total_score = (0.4 × genre_score)
            + (0.3 × mood_score)
            + (0.2 × energy_score)
            + (0.1 × tempo_score)
```

---

## How To Run
```bash
python3 recommender.py
```

## Requirements
- Python 3.x
- pandas
- scikit-learn