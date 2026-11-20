# Five-second live-human video model test (quality gate)

## Actually generated

Two genuine text-to-video renders were produced by Lightricks's public ZeroGPU LTX-2.3 demo, via GitHub Actions, with no paid API keys or credits. Both are actual MP4 moving-video streams, **not still-image animations, slideshows or Blender**.

First attempt (seed 1469) successfully generated a 5.04s 512x768 H264 + AAC movie, but **failed visual QA**: the infant developed a second apparent head in the closing frames.

Second attempt (seed 1470), after explicitly requiring a single swaddled infant and one continuous medium shot, generated a 5.04s 512x768 H264 + AAC movie. The second version has much more coherent mother-and-baby movement, period-toned earthen courtyard setting and an obvious physical camera perspective. The second supporting woman specified in the prompt was **not** clearly depicted. The infant's head is still visible despite a request that it remain covered. One distant background figure and exterior architectural details warrant review. Do not claim this is historical footage or a verified period reconstruction.

## Editorial and visual verdict

**Real-model proof achieved; professional publishable film NOT achieved.** This scene is an editorial illustration of a generic mother holding a newborn; neither her identity nor her appearance is known from contemporary records. In the final history reel, use a proper reviewed voiceover and religious/historical review, and distinguish later Janamsakhi traditions from historical consensus.

The edited MP4 adds an accurate place/year caption, gentle colour adjustment and a fully original locally synthesized Foley layer. The soundtrack contains no claimed historical ambient recording.

## Reproduce

    python -m pip install "gradio_client>=1.3,<3"
    python sikh_studio/generative_birth_5s/generate.py

After an MP4 is actually returned (never substitute a still), run:

    python -m pip install numpy scipy
    python sikh_studio/generative_birth_5s/finish.py \
       sikh_studio/generative_birth_5s/output/talwandi_1469_real_motion_test_5s.mp4

The public free GPU may be unavailable, rate-limited or require sign-in in the future. Do not silently use paid subscriptions, Runway credits, or other services. Keep drafts unlisted until human approval.
