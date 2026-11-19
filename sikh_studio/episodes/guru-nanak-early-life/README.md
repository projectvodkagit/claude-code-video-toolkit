# Guru Nanak Dev Ji — early-life pilot (45 seconds)

This is an **unapproved historical/visual draft**, not a finished public video. The script deliberately identifies traditional Janamsakhi accounts as tradition.

- `episode.json`: 8 character-led shots totaling 45 seconds.
- `sources.json`: source ledger and claim classification.
- `voice.txt`: scratch narration. Have a Sikh-history reviewer check wording and Punjabi names.
- `clips/<shot-id>.mp4`: REQUIRED rendered Blender character footage. Not included. The editor refuses to replace missing footage with image slides.
- `voice.wav`: narration audio, generated locally with `pipeline.py voice` on macOS or recorded separately.
- `music.wav` and `effects/<shot-id>.wav`: optional licensed/local background music and sound effects.

**First create an original historically appropriate Punjabi environment and review period clothing.** The upstream desk/kitchen set is a technical sample, not a publishable substitute.

From the toolkit repository root:

    python3 sikh_studio/pipeline.py validate sikh_studio/episodes/guru-nanak-early-life
    python3 sikh_studio/pipeline.py doctor

After real character clips exist, create or supply narration and then:

    python3 sikh_studio/pipeline.py render sikh_studio/episodes/guru-nanak-early-life

The output stays a preview until source, character, visual and audio reviews pass. No automatic publishing or paid generation.
