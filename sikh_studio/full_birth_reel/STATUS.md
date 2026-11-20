# Current generation status

## Requested deliverable

45-second vertical cinematic Guru Nanak Dev Ji birth reel. **The only on-screen text is the verbatim spoken voiceover**. Nine unique five-second genuinely moving model video shots (not GIFs, Blender, or still slides), plus natural Kokoro narration, original low-volume ambience, and no paid generation credits.

## Completed in this execution

- Source-based nine-shot script is version-controlled in `scenes.json`.
- Local Apache-2.0 Kokoro voice successfully generated all nine lines (success in GitHub Actions workflow run 44655212205).
- A real video model generated new village-moving shots 1 and 2 successfully, and an earlier five-second model shot is available for mother and infant (artifact run 44650529741).
- The free Hugging Face ZeroGPU demonstration responded **"You have exceeded your ZeroGPU runs limit. Authenticate with a Hugging Face token for more quota"** on shot 5. We did **not** supply tokens, bypass quotas, or use paid video credits.
- Some new generated video footage contained invented banners/text and modern-looking lighting; these scenes fail visual publication QA. The local rough-cut removes the unwanted on-screen text via reframing and compositing. It includes duplicated moving footage and is **not** the complete nine-unique-scene film.
- Full video assembly code deliberately rejects missing scene clips instead of silently substituting slides or repetitions. No false success.

## Completed local rough-cut status

An experimental 45-second narrated preview with **three distinct model-generated moving source clips** repeated across nine five-second slots was rendered locally, audio and video tracks verified, and captions checked to be exact voiceover text. This output is a *placeholder continuity edit*, NOT a finished model-generated film. Local workspace file: `guru_nanak_birth_full_45s_rough_cut.mp4` (not version-controlled or uploaded to GitHub).

## What remains to finish correctly

Generate, screen and approve unique scenes 3, 5, 6, 7, 8 and 9 with real human motion and no hallucinated text, recover natural period setting and character consistency, then run the full assembly workflow and inspect the resulting 45s video. This requires actual free model availability or separately approved alternative generation. No automatic publishing.

Sources: Macauliffe, *The Sikh Religion*, Vol I; Khushwant Singh, *A History of the Sikhs*, Vol I; analytical studies of Janamsakhi traditions. Later Daulatan and Hardial stories must remain explicitly framed as later written tradition, not independently documented events.
