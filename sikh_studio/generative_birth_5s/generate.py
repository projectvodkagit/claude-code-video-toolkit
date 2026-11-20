#!/usr/bin/env python3
"""Submit exactly one no-fee 5-second text-to-video request to Lightricks's public ZeroGPU Space.

The service is external and public. No payment keys, subscription or user credits.
Do not retry inference or fall back to static-image motion. Save a failure report if inaccessible.
"""
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
OUT.mkdir(exist_ok=True)

SPACE = "Lightricks/LTX-2-3"
PROMPT = (
    "Single uninterrupted five-second cinematic shot, actual photographic human motion, "
    "historically inspired late fifteenth century Punjabi village interior, "
    "Rai Bhoi di Talwandi in 1469. A sun-baked clay and lime-plaster home with thick "
    "timber ceiling beams, woven cotton floor mat, simple brass vessel, earthen courtyard "
    "visible through an unadorned rectangular doorway. Atmospheric natural side light, "
    "rich warm terracotta and deep indigo pigments, beautiful cinematic contrast, "
    "texture on real handwoven cloth and wood grain, human faces with anatomically "
    "correct eyes and hands, physically plausible living skin and subtle expression. "
    "An adult Punjabi mother in historically plausible plain wrapped cotton garment "
    "carefully cradles a baby fully swaddled in unbleached cloth, baby's face not shown. "
    "A second adult woman nearby slowly leans forward and carefully straightens one corner "
    "of the baby's cloth; the mother breathes, looks down at the infant and shifts "
    "the bundle naturally; hands move and maintain correct number of fingers. "
    "One continuous smooth gentle dolly-in with parallax behind both women, gentle "
    "shallow depth of field, premium grounded historical movie cinematography, "
    "subtle dust motes and realistic texture, expressive people who genuinely move, "
    "not a painting or an animated photograph. No dialogue, only quiet cloth movement "
    "and distant village activity. No text on screen, no watermarks, no magic, no glow "
    "around the child, no invented supernatural events. No modern buildings, "
    "no electrical lamps, no modern architecture, no modern Sikh religious symbols, "
    "no lavish palace, no smiling directly into camera, no stylized cartoon, no clay "
    "models. Artistic reconstruction only, not a claim about actual weather that day."
)

def save_status(status, **kwargs):
    (OUT / "status.json").write_text(json.dumps({
        "status": status,
        "service": SPACE,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cost_policy": "No paid services, tokens, accounts or credits",
        **kwargs
    }, indent=2) + "\n", encoding="utf-8")

def get_path(data):
    if isinstance(data, str) and Path(data).is_file():
        return Path(data)
    if isinstance(data, dict):
        if data.get("path") and Path(data["path"]).is_file():
            return Path(data["path"])
        for v in data.values():
            found = get_path(v)
            if found:
                return found
    if isinstance(data, (tuple, list)):
        for value in data:
            found = get_path(value)
            if found:
                return found
    return None

def run():
    if os.environ.get("HF_TOKEN"):
        raise RuntimeError("Do not pass paid or account-authenticated Hugging Face tokens to this free test")
    from gradio_client import Client
    print("Connecting to free public demonstration:", SPACE, flush=True)
    client = Client(SPACE, verbose=True)
    api = client.view_api(return_format="dict")
    names = list(api.get("named_endpoints", {}).keys())
    print("Available endpoints:", names, flush=True)
    targets = [n for n in names if "generate_video" in n]
    if not targets:
        raise RuntimeError("Public generate_video endpoint not available; refused to call an unknown endpoint")
    endpoint = targets[0]
    print("One five-second 512x768 generation requested:", endpoint, flush=True)
    # Arguments follow the original Lightricks Space app.py order:
    # input_image, prompt, duration, enhance_prompt, seed, randomize_seed, height, width.
    # No source image so this is genuine text-to-video, not still-image animation.
    job = client.submit(None, PROMPT, 5.0, False, 1469, False, 768, 512, api_name=endpoint)
    result = job.result(timeout=540)
    path = get_path(result)
    if not path:
        raise RuntimeError("Model returned no downloadable MP4. Result type: " + str(type(result)))
    video = OUT / "talwandi_1469_real_motion_test_5s.mp4"
    shutil.copy2(path, video)
    p = subprocess.run([
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration,size:stream=codec_type,codec_name,width,height",
        "-of", "json", str(video)
    ], check=True, text=True, capture_output=True)
    details = json.loads(p.stdout)
    streams = details.get("streams", [])
    duration = float(details.get("format", {}).get("duration", 0))
    if not any(s.get("codec_type") == "video" for s in streams) or duration < 3.5:
        raise RuntimeError(f"Invalid generated video: {details}")
    # A tiny verified contact sheet, never confuse it with a video deliverable.
    frames = OUT / "frames"
    frames.mkdir(exist_ok=True)
    for second in [0.5, 2, 3.5, 4.5]:
        target = frames / f"{str(second).replace('.','_')}s.jpg"
        subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
                        "-ss", str(second), "-i", str(video), "-frames:v", "1", str(target)],
                       check=True)
    save_status("success", mp4=video.name, duration=duration, ffprobe=details,
                note="Generated by a real video model. Historical set and clothes remain an artistic reconstruction.")
    print("SUCCESS:", video, "duration", duration, flush=True)

if __name__ == "__main__":
    try:
        run()
    except Exception as exc:
        save_status("failed", reason=repr(exc), note=(
            "Free public space inaccessible, out of capacity, or returned no video. "
            "No simulation, static slideshow or paid model was substituted."
        ))
        print("VIDEO MODEL FAILURE:", repr(exc), file=sys.stderr, flush=True)
        raise
