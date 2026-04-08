# Model Card – VibeFinder 1.0

---

## 1. Model Name
**VibeFinder 1.0**
A simple content-based music recommender that matches songs to a listener's mood, genre, energy, and tempo preferences.

---

## 2. Goal / Task
VibeFinder tries to predict which songs a user will enjoy based on their stated listening preferences. It does not learn from behavior — it scores every song in the catalog against a user profile and returns the top 5 best matches.

---

## 3. Data Used
- **Dataset size:** 25 songs
- **Source:** Manually curated CSV file (`data/songs.csv`)
- **Features per song:** song_id, title, artist, genre, mood, energy (0.0–1.0), tempo_bpm, danceability, acousticness, duration_sec
- **Limits:** The dataset is small and unevenly distributed. Pop has 7 songs (28%) while genres like Classical and Latin have only 1 song each. This means Pop users get much better recommendations than users of less-represented genres.

---

## 4. Algorithm Summary
Every song gets a score out of 5.0 points based on how well it matches the user's preferences:

- **+2.0 points** if the song's genre matches the user's favorite genre
- **+1.5 points** if the song's mood matches the user's favorite mood
- **Up to +1.0 points** based on how close the song's energy is to the user's target energy (the closer, the more points)
- **Up to +0.5 points** based on how close the song's tempo is to the user's target tempo

All 25 songs are scored, then sorted from highest to lowest. The top 5 are recommended. Think of it like a judge at a talent show scoring each performer — the highest scores win.

---

## 5. Observed Behavior / Biases

**Genre dominance creates a filter bubble.**
Because genre is worth +2.0 points, a Pop song with low energy will almost always beat a perfect-energy Rock song for a Pop user. The system can recommend songs that "feel wrong" because the genre label carries too much weight compared to how the song actually sounds.

**Dataset imbalance hurts niche users.**
Pop users have 7 songs to match against. Classical users have 1. During testing, the Classical Intensity profile recommended Bohemian Rhapsody (a Rock song) as its #1 result because there weren't enough Classical songs to compete.

**Mood matching is all-or-nothing.**
"Happy" and "Energetic" are emotionally similar but score zero overlap in this system. A user wanting "Energetic" gets no credit for a "Happy" song even if it would actually fit their vibe.

**Conflicting preferences produce unexpected results.**
A user profile with high energy (0.9) but sad mood got Someone Like You by Adele as the top recommendation — a very quiet, slow song — because genre and mood matched perfectly and outweighed the energy mismatch.

---

## 6. Evaluation Process
Five user profiles were tested:

| Profile | Purpose |
|---|---|
| High-Energy Pop | Baseline — standard pop listener |
| Chill Lofi | Tests low energy and acoustic preferences |
| Deep Intense Rock | Tests cross-genre mood matching |
| High Energy but Sad | Edge case — conflicting preferences |
| Classical Intensity | Edge case — underrepresented genre |

One experiment was also run: the genre weight was halved (2.0 → 1.0) and energy weight was doubled (1.0 → 2.0) while keeping the max score at 5.0. This produced more cross-genre recommendations and surfaced Hip-Hop songs for the Rock profile because their energy scores were closer to the target.

---

## 7. Intended Use and Non-Intended Use

**Intended use:**
- Educational tool for learning how content-based filtering works
- Demonstrating how weighted scoring affects recommendation diversity
- A starting point for building more sophisticated recommenders

**Not intended for:**
- Real-world music discovery (dataset is too small)
- Replacing platforms like Spotify or YouTube Music
- Making recommendations for users with complex or evolving tastes
- Any commercial use

---

## 8. Ideas for Improvement
1. **Balance the dataset** — Add more songs per genre so niche users get fair recommendations
2. **Add a mood similarity matrix** — Award partial points for emotionally adjacent moods (e.g., "Happy" and "Energetic" should score 0.7 instead of 0.0)
3. **Incorporate listening history** — Track skips and replays so the system learns and adapts over time instead of always giving the same results

---

## Personal Reflection

**What was your biggest learning moment?**
The biggest surprise was discovering how much genre and mood dominate the scoring. I assumed energy would be the strongest "vibe" indicator — the difference between a workout song and a bedtime song is mostly about energy. But because genre and mood together are worth 3.5 out of 5.0 points, a slow quiet song in the right genre can easily beat a high-energy song in the wrong genre. That gap between what I expected and what actually happened taught me that the weights you choose are as important as the algorithm itself.

**How did using AI tools help, and when did you need to double-check them?**
AI tools helped me move fast — generating the dataset, scaffolding the code structure, and explaining concepts like `.sort()` vs `sorted()` in plain language. But I had to double-check the math every time weights changed to make sure the maximum score stayed at 5.0. AI is great at writing code quickly but doesn't always catch whether the logic makes real-world sense.

**What surprised you about how simple algorithms can still "feel" like recommendations?**
Even with just four features and basic math, the system produced results that felt surprisingly reasonable. Levitating and Blinding Lights consistently topped the Pop/Energetic profile — which is exactly what you'd expect. It was striking that something so simple could produce results that feel intelligent, even though it's just addition and sorting under the hood.

**What would you try next?**
I would add a feedback loop — letting users thumbs up or thumbs down recommendations so the weights adjust automatically over time. I'd also add valence (a happy/sad continuous scale) as a fifth feature, since it's one of the most predictive features in real music recommenders like Spotify. Finally I'd expand the dataset to at least 100 songs with balanced genre representation.