#!/usr/bin/env python3
import json,pathlib
import soundfile as sf
from kokoro_onnx import Kokoro
h=pathlib.Path(__file__).resolve().parent
scenes=json.loads((h/"scenes.json").read_text())["scenes"]
if not pathlib.Path("kokoro-v1.0.onnx").is_file() or not pathlib.Path("voices-v1.0.bin").is_file():
 raise SystemExit("Local natural Kokoro model missing; do not fall back to robotic speech")
speaker=Kokoro("kokoro-v1.0.onnx","voices-v1.0.bin")
target=pathlib.Path("work/audio");target.mkdir(parents=True,exist_ok=True)
info=[]
for s in scenes:
 samples,rate=speaker.create(s["narration"],voice="am_michael",speed=1.08,lang="en-us")
 file=target/f"voice_{s['shot']:02d}.wav";sf.write(file,samples,rate)
 print(f"Narration {s['shot']:02d} {len(samples)/rate:.2f}s: {s['narration']}",flush=True)
 info.append({"shot":s["shot"],"spoken":s["narration"],"seconds":len(samples)/rate})
(target/"timings.json").write_text(json.dumps(info,indent=2)+"\n")
