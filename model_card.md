# Model Card – Music Recommender Simulation

## Model Overview
A content-based music recommender system built in Python. It scores songs against a user preference profile using a weighted point system across genre, mood, energy, and tempo. The top 5 scored songs are returned as recommendations.

---

## Intended Use
- Educational simulation of how content-based filtering works
- Demonstrating the tradeoffs between categorical and numerical feature matching
- Exploring how weight adjustments affect recommendation diversity

---

## How It Works
Each song is scored out of 5.0 points:
| Feature | Points | Type |
|---|---|---|
| Genre match | +1.0–2.0 | Exact categorical match |
| Mood match | +1.5 | Exact categorical match |
| Energy similarity | up to +2.0 | Continuous numerical score |
| Tempo similarity | up to +0.5 | Continuous numerical score |

---

## Limitations and Bias

**1. Genre Dominance Creates a Filter Bubble**
The genre feature carries the most weight in the scoring formula, which means users who prefer less-represented genres (like Classical or Latin) receive poor recommendations because so few songs in the dataset match their genre. During stress testing, the Classical profile's top recommendation was a Rock song simply because no Classical songs had matching energy scores.

**2. Dataset Imbalance Favors Pop Users**
Approximately 28% of the 25-song dataset is Pop music, meaning Pop users consistently receive higher-quality recommendations than users of underrepresented genres. A real-world system would require a much more balanced dataset or genre-normalized scoring to avoid this disparity.

**3. Binary Mood Matching Ignores Emotional Proximity**
Mood matching is all-or-nothing — a song labeled "Happy" earns zero mood points for a user who wants "Energetic," even though these moods are emotionally adjacent. A more sophisticated system would use a mood similarity matrix to award partial points for related moods.

**4. No Listening History or Feedback Loop**
The system relies entirely on stated user preferences with no ability to learn from actual listening behavior. Real recommenders improve over time by incorporating skips, replays, and playlist additions. This system will always recommend the same songs for the same profile with no personalization over time.

**5. Linear Energy Penalty May Not Reflect Perception**
The energy similarity formula applies an equal penalty across the entire 0.0–1.0 scale. However, the perceptual difference between energy 0.8 and 0.9 may feel much smaller to a listener than the difference between 0.1 and 0.2, suggesting a logarithmic or curved similarity function might be more accurate.

---

## Experiment Results

### Weight Shift Experiment
Doubling energy weight (1.0 → 2.0) and halving genre weight (2.0 → 1.0) while keeping max score at 5.0 produced more cross-genre recommendations. The Deep Intense Rock profile surfaced Hip-Hop songs (Sicko Mode, Lose Yourself) ahead of some Rock songs because their energy scores were closer to the target. This suggests energy is a stronger "vibe" indicator than genre alone.

### Edge Case Findings
- **High Energy but Sad:** Someone Like You (energy 0.3) ranked #1 for a user wanting energy 0.9, purely due to genre + mood points. This confirms genre dominance bias.
- **Classical Intensity:** Bohemian Rhapsody ranked #1 over Moonlight Sonata for a Classical user because dramatic mood + high energy outweighed genre matching.

---

## Recommendations for Improvement
# Model Card – Music Recommender Simulation

## Model Overview
A content-based music recommender system built in Python. It scores songs against a user preference profile using a weighted point system across genre, mood, energy, and tempo. The top 5 scored songs are returned as recommendations.

---

## Intended Use
- Educational simulation of how content-based filtering works
- Demonstrating the tradeoffs between categorical and numerical feature matching
- Exploring how weight adjustments affect recommendation diversity

---

## How It Works
Each song is scored out of 5.0 points:
| Feature | Points | Type |
|---|---|---|
| Genre match | +1.0–2.0 | Exact categorical match |
| Mood match | +1.5 | Exact categorical match |
| Energy similarity | up to +2.0 | Continuous numerical score |
| Tempo similarity | up to +0.5 | Continuous numerical score |

---

## Limitations and Bias

**1. Genre Dominance Creates a Filter Bubble**
The genre feature carries the most weight in the scoring formula, which means users who prefer less-represented genres (like Classical or Latin) receive poor recommendations because so few songs in the dataset match their genre. During stress testing, the Classical profile's top recommendation was a Rock song simply because no Classical songs had matching energy scores.

**2. Dataset Imbalance Favors Pop Users**
Approximately 28% of the 25-song dataset is Pop music, meaning Pop users consistently receive higher-quality recommendations than users of underrepresented genres. A real-world system would require a much more balanced dataset or genre-normalized scoring to avoid this disparity.

**3. Binary Mood Matching Ignores Emotional Proximity**
Mood matching is all-or-nothing — a song labeled "Happy" earns zero mood points for a user who wants "Energetic," even though these moods are emotionally adjacent. A more sophisticated system would use a mood similarity matrix to award partial points for related moods.

**4. No Listening History or Feedback Loop**
The system relies entirely on stated user preferences with no ability to learn from actual listening behavior. Real recommenders improve over time by incorporating skips, replays, and playlist additions. This system will always recommend the same songs for the same profile with no personalization over time.

**5. Linear Energy Penalty May Not Reflect Perception**
The energy similarity formula applies an equal penalty across the entire 0.0–1.0 scale. However, the perceptual difference between energy 0.8 and 0.9 may feel much smaller to a listener than the difference between 0.1 and 0.2, suggesting a logarithmic or curved similarity function might be more accurate.

---

## Experiment Results

### Weight Shift Experiment
Doubling energy weight (1.0 → 2.0) and halving genre weight (2.0 → 1.0) while keeping max score at 5.0 produced more cross-genre recommendations. The Deep Intense Rock profile surfaced Hip-Hop songs (Sicko Mode, Lose Yourself) ahead of some Rock songs because their energy scores were closer to the target. This suggests energy is a stronger "vibe" indicator than genre alone.

### Edge Case Findings
- **High Energy but Sad:** Someone Like You (energy 0.3) ranked #1 for a user wanting energy 0.9, purely due to genre + mood points. This confirms genre dominance bias.
- **Classical Intensity:** Bohemian Rhapsody ranked #1 over Moonlight Sonata for a Classical user because dramatic mood + high energy outweighed genre matching.

---

## Evaluation Summary

Five profiles were tested: High-Energy Pop, Chill Lofi, Deep Intense Rock, High Energy but Sad, and Classical Intensity. The most surprising finding was that the High Energy but Sad edge case ranked Someone Like You (energy 0.3) as the top recommendation for a user targeting energy 0.9, purely because genre and mood together contributed 3.5 out of 5.0 points before energy was factored in. The Classical Intensity profile revealed a dataset imbalance problem — with only one Classical song available, the system defaulted to cross-genre recommendations. The Deep Intense Rock profile unexpectedly surfaced Hip-Hop songs ahead of Rock songs because mood matching (+1.5) compensated for the genre mismatch. Overall the system works well for Pop users but struggles with underrepresented genres.

---

## Recommendations for Improvement
- Add more songs per genre to balance the dataset
- Implement a mood similarity matrix for partial mood matching
- Incorporate user feedback signals (likes, skips) for adaptive recommendations
- Consider logarithmic energy scaling for more perceptually accurate similarity
- Add a valence feature (happy/sad continuous scale) for richer emotional matching