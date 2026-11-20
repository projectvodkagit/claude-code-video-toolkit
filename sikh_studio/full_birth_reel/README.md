# Full 45-second Guru Nanak birth cinematic reel

This version uses nine distinct five-second genuine moving AI-video shots (eight new free LTX-2.3 generations and one previously verified 5s birth clip), offline natural Kokoro TTS, original ambient sound and captions that reproduce **only the spoken voiceover**, word for word. No title cards, source overlays, place labels, logos or credits on-screen.

Sources: Max Arthur Macauliffe, *The Sikh Religion* Volume I, Life of Guru Nanak Chapter I; Khushwant Singh, *A History of the Sikhs* Volume I; Sikh Missionary Society's *Janamsakhi Tradition: An Analytical Study*. The Daulatan and Hardial statements are framed as descriptions in **later Janamsakhi tradition**, not contemporary eyewitness evidence.

The design of village, costume, gestures and weather are all visual artistic reconstruction. Do not describe them as confirmed details of the date. The next-morning Hardial account is explicitly kept after the birth.

The video engine is the public free Lightricks LTX-2.3 video-model demo, and the voice model is Kokoro-82M (Apache-2.0 weights). Public queue can be rate-limited. No paid API keys or credit consumption. No automatic publishing. Maintain cultural accuracy and natural human motion; check each generated shot for anatomy and scene continuity. If any generated footage fails, do not substitute Blender, slideshow, still-image parallax or unrelated footage.

Files:
- `scenes.json`: exact narration and source-linked shot plan; source of subtitle words
- `generate_one.py`: exactly one free model request per shot
- `narrate.py`: offline Kokoro voice
- `assemble.py`: checks all nine clips and audio, captions from voiceover only, and delivers MP4
- `.github/workflows/guru-nanak-full-45s.yml`: GitHub generation, narration, assembly, QA and artifact delivery
