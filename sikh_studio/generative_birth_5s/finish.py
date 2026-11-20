#!/usr/bin/env python3
"""Reproduce the five-second proof's restrained editorial treatment and original Foley.
Usage from repo root:
  python sikh_studio/generative_birth_5s/finish.py \
    sikh_studio/generative_birth_5s/output/talwandi_1469_real_motion_test_5s.mp4
Requires: ffmpeg, numpy, scipy. Does NOT use any paid API or image/video generation.
"""
import argparse
import subprocess
from pathlib import Path
import numpy as np
from scipy import signal
from scipy.io import wavfile

HERE = Path(__file__).resolve().parent
P = argparse.ArgumentParser()
P.add_argument("input", type=Path)
P.add_argument("--output", type=Path, default=HERE / "output" / "talwandi_5sec_edited.mp4")
args = P.parse_args()
if not args.input.is_file():
    raise SystemExit("Actual model-rendered MP4 required; still-image substitutes forbidden")
args.output.parent.mkdir(parents=True, exist_ok=True)
sr, dur = 48000, 5.08
n = round(sr * dur)
rng = np.random.default_rng(1469)
noise = rng.standard_normal(n)
low = signal.sosfilt(signal.butter(3, 720, fs=sr, output="sos"), noise)
low /= max(np.std(low), 1e-6)
slow = np.sin(2 * np.pi * np.arange(n) / sr * .31) * .14 + .86
out = low * .006 * slow
for start, length, level in [(1.02, .38, .038), (2.02, .44, .031), (3.46, .30, .033), (4.20, .27, .016)]:
    i, jj = int(start * sr), int(length * sr)
    j = min(n, i + jj)
    rustle = signal.sosfilt(signal.butter(2, [650, 4400], fs=sr, btype="bandpass", output="sos"), rng.standard_normal(j - i))
    rustle /= max(np.std(rustle), 1e-6)
    env = np.sin(np.linspace(0, np.pi, j - i)) ** 1.4
    out[i:j] += rustle * env * level
fade = int(.30 * sr)
out[-fade:] *= np.linspace(1, 0, fade)
peak = float(np.max(np.abs(out)))
if peak > .89:
    out *= .89 / peak
foley = args.output.parent / "original_foley.wav"
wavfile.write(foley, sr, (out * 32767).astype(np.int16))
vf = ("[0:v]crop=432:768:0:0,scale=720:1280:flags=lanczos,"
      "eq=contrast=1.035:saturation=1.04,"
      "drawbox=x=0:y=1030:w=720:h=250:color=0x110F0C@0.33:t=fill,"
      f"ass={HERE / 'captions.ass'}[v];"
      "[0:a]volume=12dB[a0];[1:a]volume=0.63[a1];"
      "[a0][a1]amix=inputs=2:duration=first:normalize=0,"
      "alimiter=limit=0.90[a]")
cmd = [
    "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
    "-i", str(args.input), "-i", str(foley),
    "-filter_complex", vf, "-map", "[v]", "-map", "[a]",
    "-c:v", "libx264", "-crf", "17", "-preset", "medium",
    "-pix_fmt", "yuv420p", "-r", "24", "-t", "5.041667",
    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart",
    str(args.output),
]
subprocess.run(cmd, check=True)
print("Finished edited real-model video:", args.output)
