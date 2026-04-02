Reflection – Music Recommender Evaluation
Overview
I tested five user profiles against a 25-song dataset to evaluate how well my content-based recommender handles diverse listening preferences. Here's what I found in plain language — no coding experience required to follow along.

Profile Comparisons
🎵 High-Energy Pop vs. 😌 Chill Lofi
The High-Energy Pop profile consistently scored Pop songs at 4.7–4.9 out of 5.0, with Levitating and Blinding Lights dominating the top spots. The Chill Lofi profile found one near-perfect match (Redbone at 4.78) but then dropped sharply — songs 2 through 5 all scored below 1.5.

Why this makes sense: The dataset has 7 Pop songs but only 1 R&B song. The Chill Lofi user essentially ran out of good matches after Redbone. It's like walking into a store where 7 out of 10 items on the shelf are in one style — if that's not your style, you're left with very few good options. This is a clear example of dataset imbalance favoring Pop users.

🤘 Deep Intense Rock vs. ⚡ High Energy but Sad
The Rock profile was surprising — Hip-Hop songs (Sicko Mode, Lose Yourself, HUMBLE.) ranked in the top 5 ahead of Hotel California. This is because all three Hip-Hop songs had an "Intense" mood matching the profile, which earned them +1.5 points that Hotel California didn't get.

The High Energy but Sad profile produced the most unexpected result of all: Someone Like You by Adele ranked #1 even though the user wanted high energy (0.9) and Adele's song has very low energy (0.3). How? Because genre (Pop) and mood (Sad) together gave it 3.5 points before energy was even considered.

Why this makes sense: Imagine you're looking for an intense workout song but you also said you love sad Pop music. The system found the "saddest Pop song" in the database and gave it top marks — even though you'd never actually want to hear Adele at the gym. This shows that when two features strongly agree (genre + mood), they can overpower a feature that might matter more in real life (energy).

🎹 Edge Case – Classical Intensity
This profile was designed to stress test the system. A user who loves Classical music with high energy (0.9) got Bohemian Rhapsody by Queen as their #1 recommendation — a Rock song, not Classical. Moonlight Sonata (the only Classical song in the dataset) ranked #2 despite being a perfect genre match, because its energy (0.1) was far from the target (0.9).

Why this makes sense: Think of it like a restaurant recommender that only has one Italian dish on the menu. If that dish doesn't match what you're hungry for today, the system starts recommending Mexican food instead because it's closer to your mood. Having only one Classical song in the dataset means Classical users will almost always get cross-genre recommendations.

What Surprised Me Most
The biggest surprise was how much genre and mood dominated the scoring. I expected energy to be the strongest "vibe" indicator — after all, the difference between a workout song and a bedtime song is mostly energy. But because genre and mood are worth a combined 3.5 points out of 5.0, a low-energy song in the right genre can easily beat a high-energy song in the wrong genre.

This is exactly how a "Gym Hero" song keeps showing up for Happy Pop users. If the song is Pop and labeled Happy, it earns 3.5 points immediately — even if it's slow and quiet. The system doesn't know you're at the gym. It just sees "Pop" and "Happy" and gives it full marks before even looking at the beat.

What I Would Change
If I were building this for real users I would:

Lower genre weight and raise energy weight so the "vibe" matters more than the label
Add more songs per genre so niche users get fair recommendations
Build in a mood similarity scale so "Happy" and "Energetic" aren't treated as completely different
Track listening history so the system learns from what users actually skip or replay
