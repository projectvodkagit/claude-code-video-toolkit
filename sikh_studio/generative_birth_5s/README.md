# Five-second, real human motion model test

This is the **replacement for failed clay Blender and flat motion graphics prototypes**.

It attempts one external free publicly queued generation using Lightricks's official [LTX-2.3 ZeroGPU Hugging Face demo](https://huggingface.co/spaces/Lightricks/LTX-2-3). The demo currently advertises a free GPU-based text-to-video endpoint. The public queue may be inaccessible, slow or subject to login / daily quotas; **this is not a paid API and it is not guaranteed**.

## Artistic direction
Five seconds inside a plausibly reconstructed simple village house in Talwandi around 1469. Mother holds a swaddled infant; second adult adjusts cloth. People actually act: hands move, faces respond, fabric moves and camera travels. No direct speech, supernatural effects or 17th-century architecture. This depiction is an artistic interpretation, not a documented likeness or a precise weather record.

## How to run

From the repository root in an internet-enabled environment:

    python -m pip install gradio_client
    python sikh_studio/generative_birth_5s/generate.py

When invoked from GitHub Actions, artifact `historical-human-motion-five-second-test` contains the MP4 and QA frames if the model worked, otherwise a status JSON with an error. **Never claim success or substitute a still slideshow after a failure.**

Do not spend Runway, HeyGen or any API credit, create paid GPU sessions, or use account tokens. This test is not approved for publication without historical and visual review.

## What should pass the quality gate

- Human hands/faces correctly shaped across frames
- Mother and second woman's gestures clearly move and maintain continuity
- The camera creates genuine physical depth rather than a pushed still
- Earthen period interior, no modern or Khalsa-era religious iconography
- The baby stays fully swaddled with no uncanny portrait
- Video lasts approximately five seconds with live motion
