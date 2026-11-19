# Standing production instructions for all future Sikh History reels

These decisions were made in chat and must persist across sessions:

1. Every factual claim in narration must be tied to an identifiable *written* source and distinguish contemporaneous evidence, scholarly conclusions and later Sikh religious tradition. Never invent direct quotations, miracles, or private thoughts.
2. Preserve a single historically plausible timeline. For the 1469 Guru Nanak birth reel stay within Rai Bhoi di Talwandi in Punjab and the immediate period after his birth. If the next morning is shown, label the time shift. Do not imply precise real weather conditions from an artistic reconstruction.
3. The birth year 1469, parents Tripta and Mehta Kalu, and Talwandi come from Macauliffe (The Sikh Religion, Volume I, Life of Guru Nanak Chapter I) and historical scholarship. Source URLs in sources.md.
4. Janamsakhi mentions of Daulatan and Hardial are **traditional accounts**, not verified contemporary eyewitness reports. Make this distinction visible on screen as well as in narration.
5. No modern gurdwara domes, Nishan Sahib, five Ks, Khalsa-era regalia, electric lighting, modern clothing, fantasy visual effects, or modern Punjab architecture in a 1469 reconstruction.
6. Use physically moving, **rigged** characters in a designed 3D environment. Do not pass off parallax pans, Ken Burns photos, still galleries or GIFs as filmed character animation. The style should be cohesive across episodes.
7. Reuse cast definitions, colour palette, environment assets, camera style, motion pacing, and voice rules.
8. Produce complete deliverables: 9:16 MP4 with narration, original/licensed music and Foley, timed readable captions, editable source, QA report and source notes.
9. No paid video, image, voice, music credits or API calls without explicit advance approval. No automatic publishing.
10. Do not misrepresent renderer availability or export checks. Verify every MP4 has the expected duration, live motion and an audible audio stream.
11. Historical scenes are visual **reconstructions**, not documented likenesses. The swaddled infant is a symbolic depiction, not a verified portrait of Guru Nanak Dev Ji.
12. Keep written-source and visual-accuracy review open before publishing. Source editions/page references should be confirmed against printed texts.

Production command on a machine with Blender, FFmpeg and eSpeak:

    blender -b -t 2 --python sikh_studio/birth_reel/render_birth.py -- --out build/birth1469_silent.mp4
    python3 sikh_studio/birth_reel/postproduce.py --input build/birth1469_silent.mp4 --output build/guru_nanak_birth_1469_reel.mp4

GitHub Actions workflow: .github/workflows/sikh-birth-reel.yml; downloads finished reel as an artifact.
