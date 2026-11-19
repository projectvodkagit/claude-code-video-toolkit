# Sikh History Studio: the explainer production engine

## Decision

Use [HyperFrames](https://github.com/heygen-com/hyperframes) as the primary motion-graphics renderer, not the custom Blender village renderer. HyperFrames is Apache-2.0-licensed, provides HTML/CSS/GSAP timing, reusable title/map/timeline layers, audio tracks and an MP4 exporter. Pair it with [explainer-video-opus-5.5](https://github.com/RohanRatwani/explainer-video-opus-5.5) (MIT) as an optional agent-run research, voice and storyboard method, not as a prerequisite or paid API.

**Keep the existing history ledger and rules.** This repo already holds an episode manifest, sources and editorial guidance. Do not redo or erase those.

## Why the previous video failed the style goal

The clay-style Blender version was a bare 3D environment with elementary characters and camera movement. It lacked animated graphics, map layers, visual transitions, information hierarchy, compelling captions, motion-design pacing and premium narration.

The fix is not more camera motion in the same clay set. It is a motion-graphics-first animation pipeline that can incorporate approved actors/illustrations as one layer.

## Quality target

Every reel needs:

- Opening visual hook within the first two seconds.
- A distinctive editorial palette and typography.
- Several independent animated layers per sequence (map, people, labels, dates, scene atmosphere).
- Caption-safe zones and source labels; no overlapping text.
- Meaningful motion linked to narration, not random scrolling or static-slide zooms.
- An original or properly licensed soundtrack, clean voice and carefully placed Foley.
- 9:16 preview and full MP4 export, each inspected with a contact sheet.
- A historical script whose facts can be traced to a source, distinguishing later Janamsakhi tradition from established history.
- Reusable visual tokens and character illustrations for the next film.

## Pilot

`sikh_studio/hyperframes_birth/index.html` is a 14-second technical/style sample. It demonstrates animated typography, a *schematic* location map, graphic character illustrations, evidence labels, gesture animations and an audio timeline.

This is **not** a finished 45-second reel and the characters are **not** realistic actors. The map is decorative and not a surveyed historical cartographic reconstruction. No weather claims or fabricated dialogue. No paid API credits.

The generated sample is built using GitHub Actions in `.github/workflows/sikh-hyperframes-proof.yml`. You can also use these commands in the pilot directory after installing Node 22+ and FFmpeg:

    npx hyperframes lint
    npx hyperframes render --output hyperframes-nanak-proof.mp4 --fps 30 --quality draft --workers 1

The offline `espeak` voice is a timing placeholder. For publishing, replace it with a high-quality licensed voice (including local Kokoro if its specific model licence permits the use).

## Licences

- HyperFrames: Apache-2.0, commercial use allowed under licence conditions.
- RohanRatwani/explainer-video-opus-5.5: MIT.
- EDStudio: PolyForm Noncommercial; *do not* copy its code, animation or example media into a monetized production without permission.
- Anything2Explainer: PolyForm Noncommercial; same caution.
- Third-party TTS voices, music, 3D models and photos have their own licences. Check each separately.

## What is still missing

We need production-quality character artwork and genuine human acting where the episode calls for it. HyperFrames animates and composites graphical elements, but it is **not** a generative actor video model. A reusable visual cast, period-correct settings and historical approval are separate production tasks. Do not claim they are solved by switching the renderer.

The next milestone is to expand the approved 14-second visual language into a 45-second narrative, review the script and scene art, sync a proper voice, and test on 9:16 before publication.
