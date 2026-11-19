# Sikh History Reel Studio

**Installed in this fork of Digital Samba's MIT-licensed video toolkit.** We reuse its code-first Blender character renderer, Remotion editor and audio tooling rather than building a replacement slideshow renderer.

## What exists

A 45-second Guru Nanak Dev Ji episode manifest with eight character-led shots, an editorial source ledger, reusable cast colour/seed records, a free/local FFmpeg mixer, scratch macOS narration support, tests and a generic **six-second rig test**. Neither the generic rig test nor the story manifest proves a historically accurate costume or period village.

## What is not ready

Actual 15th-century Punjabi environment assets, finished character scenes, publication-quality narration, and final religious/historical review. This studio does not call paid video/voice APIs or publish automatically.

## On your Mac (from repo root)

Install FFmpeg and Blender, then install upstream dependencies:

    brew install uv ffmpeg
    brew install --cask blender
    uv sync
    python3 sikh_studio/pipeline.py doctor
    python3 -m unittest discover -s sikh_studio/tests -v
    uv run tools/blender_render.py doctor --no-bench
    uv run tools/blender_render.py check sikh_studio/smoke/blender-motion-test.json

Optional generic rig animation test (not period footage):

    uv run tools/blender_render.py render sikh_studio/smoke/blender-motion-test.json

See `sikh_studio/docs/PRODUCER_INSTRUCTIONS.md` and the episode directory. The assistant should create and check a historically reviewed village set, then render eight clips with real character acting and assemble them with narration, effects and music.

## Production

    python3 sikh_studio/pipeline.py validate sikh_studio/episodes/guru-nanak-early-life
    python3 sikh_studio/pipeline.py voice sikh_studio/episodes/guru-nanak-early-life --rate 155
    python3 sikh_studio/pipeline.py validate sikh_studio/episodes/guru-nanak-early-life --require-assets
    python3 sikh_studio/pipeline.py render sikh_studio/episodes/guru-nanak-early-life

The last two commands intentionally fail until **every** moving MP4 shot and `voice.wav` exist. Audio can include `music.wav` and per-shot `effects/<id>.wav`. No slideshow fallback.

**Costs:** the code and offline tests have no video generation API charges. Realistic local 3D animation requires Blender and rendering time on your Mac. Any future paid provider must be approved separately.
