# Birth of Guru Nanak Dev Ji  -  1469

This is a **45-second, 9:16, original stylized 3D reconstruction**, generated with Blender and edited using FFmpeg. Unlike the older slideshow draft, characters have articulated rigs, real motion, moving cameras and modeled environments.

- `render_birth.py`: procedural Punjabi village, household interior and animated characters; no external asset API.
- `narration.txt`: factual voice script; no invented dialogue.
- `captions.ass`: timed subtitles and explicit label for Janamsakhi material.
- `postproduce.py`: offline original drone/ambience, eSpeak scratch voice, subtitle burn, MP4.
- `sources.md`: written references and levels of certainty.
- `AGENTS.md`: instructions carried forward for all videos.

## Export

Run `blender -b -t 2 --python sikh_studio/birth_reel/render_birth.py -- --out build/birth1469_silent.mp4`

Then `python3 sikh_studio/birth_reel/postproduce.py --input build/birth1469_silent.mp4 --output build/guru_nanak_birth_1469_reel.mp4`.

On GitHub Actions, choose the workflow named **Nanak birth: generate a 3D narrated reel** and download the produced video artifact after a successful run.

This is a draft visual reconstruction, not a verified portrait or an independently authenticated 15th-century environment. Improve costumes/architecture against visual historical reference before publishing. Do not assume actual recorded weather.

No paid AI API or credit usage. Rendering uses ordinary GitHub Actions CPU time; usage limits depend on repository settings. Workflows do not automatically upload to YouTube/Instagram.
