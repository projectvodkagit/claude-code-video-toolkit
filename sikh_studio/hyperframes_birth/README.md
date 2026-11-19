# 14-second graphic-rich Sikh-history proof

This is a new HyperFrames-based 9:16 reel prototype: animated map, kinetic typography, layered illustrated characters with gesture movement, evidence labels, voiceover, and a golden-ink style. It is not a realistic character-acting film and it does not use synthetic video-generation credits.

## Run

Install Node 22+ and FFmpeg, generate (or supply) `voice.wav`, then:

    npx --yes hyperframes lint
    npx --yes hyperframes render --output nanak-motion-proof.mp4 --fps 30 --workers 1

The project is written to be re-authored into a 45-second episode after the 14-second look is approved. The original `sikh_studio/birth_reel/sources.md` and its research restrictions remain authoritative.

## Notes

External GSAP from jsDelivr requires a network fetch during browser rendering; for offline production, install/pin it locally. Data drawn in the map is decorative, **not a surveyed 1469 map**; the label explains that it is an illustration. No claim is made about the weather or an eyewitness account of the birth.