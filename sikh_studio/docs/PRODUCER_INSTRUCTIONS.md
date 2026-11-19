# Sikh history video producer — Codex / ChatGPT instructions

Read these instructions and the upstream toolkit's \`AGENTS.md\`, \`CLAUDE.md\`, \`docs/blender.md\` and \`.claude/skills/blender/SKILL.md\` before changing any video engine code.

## Non-negotiable production rules

- Films must feature actual rigged 3D movement or other real motion footage. A still photograph with a pan/zoom, synthetic GIF slide or montage is not a character animation and must not replace a missing scene.
- Maintain a reusable cast with identical rig/seed/colour definitions in \`kits/sikh-history/cast\`. These are stylized concepts, not authenticated likenesses; period dress requires historical review.
- Create an original 15th-century Punjab village environment; the upstream desk and kitchen examples are **engineering tests**, not acceptable substitutes for a historical village.
- Fact-check each narrated claim against \`episodes/*/sources.json\`. Janamsakhi birth and sacred-thread accounts must be introduced as traditions; don't invent direct Guru quotations. Obtain editorial/religious approval before publication.
- Absolutely no paid video, voice, image or music API calls, including trial-credit usage, without explicit permission. Never auto-publish or schedule.
- Audio must include voice narration; music and Foley are optional, licensed tracks. No unlicensed commercial songs. Mix music below voice.
- All 8 episode scene clips must be real MP4 footage. The pipeline refuses missing video and never substitutes slides. This is intentional.

## First engineering task

From the toolkit root:

    python3 sikh_studio/pipeline.py doctor
    python3 -m unittest discover -s sikh_studio/tests -v
    uv sync
    uv run tools/blender_render.py doctor --no-bench
    uv run tools/blender_render.py check sikh_studio/smoke/blender-motion-test.json
    uv run tools/blender_render.py render sikh_studio/smoke/blender-motion-test.json

The smoke spec tests generic character movement only. Once its contact sheet shows moving poses, create a period-correct village set with real character actions and camera moves. Validate every \`spec.json\` with the upstream Blender checker before rendering.

## Finished pilot

Draft narration lives in \`sikh_studio/episodes/guru-nanak-early-life/voice.txt\`. A macOS scratch voice can be generated with:

    python3 sikh_studio/pipeline.py voice sikh_studio/episodes/guru-nanak-early-life --rate 155

For a genuine preview, render the eight approved moving character shots as MP4 into the episode's \`clips/\` directory, provide \`voice.wav\` and optional \`music.wav\` and \`effects/<shot-id>.wav\`, then:

    python3 sikh_studio/pipeline.py validate sikh_studio/episodes/guru-nanak-early-life --require-assets
    python3 sikh_studio/pipeline.py render sikh_studio/episodes/guru-nanak-early-life

Review sound synchronisation, character acting, hands, costumes, sources and narration, including Punjabi pronunciation, before publication. 45-second preview is not automatically finished production.

## Formats

9:16 for reels, 16:9 for 10–15 minute YouTube chapters. A long film should be divided into approved clip batches, with reusable cast and environment assets and a single audio master; do not promise local M1 rendering will be fast.
