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
    "Single uninterrupted five-second premium historical movie shot, genuinely moving "
    "humans, a simple domestic room in the Punjabi village of Rai Bhoi di Talwandi "
    "in the year 1469. Rich and filmic earthy pigments, burnt umber, faded madder red "
    "and muted deep indigo, soft amber indirect light and beautiful deep shadows. "
    "Hand-plastered earthen walls, ancient rough timber ceiling beams, a flat wooden "
    "door opening into a small mud-walled courtyard, handcrafted copper water vessel, "
    "low woven charpoy, no glass windows or contemporary urban buildings. "
    "A Punjabi mother in a natural handwoven draped cotton shawl sits by the cot "
    "holding exactly one small newborn. The single baby is a featureless tightly "
    "wrapped small cotton bundle with the head and face hidden under a clean fold of "
    "cloth; no infant skin, head, or fingers visible, no additional children. "
    "A second adult woman in a simple period-appropriate cotton wrap leans in "
    "slightly, gently adjusts the outer corner of the same bundle, then withdraws "
    "one hand with believable shoulder and elbow movement. The mother looks down "
    "at the cloth bundle the entire time; her breathing shifts it slightly, "
    "and her hands carefully change their grip. One realistic interaction, "
    "natural human anatomy and correct number of hands and fingers throughout. "
    "One continuous medium-wide two-person composition, slow controlled "
    "sideways dolly movement with real parallax, subject stays visible, no sudden "
    "cuts, no tight close-up of the bundle. Very high quality cinematic drama "
    "photography, natural film grain and realistic textile fibers. Gentle cloth "
    "rustling and distant faint ambient courtyard sounds, no dialogue. "
    "This is a respectful fictional artistic reconstruction, not an eyewitness "
    "record. No modern gurdwaras, no Khalsa-era costumes or symbols, no modern "
    "architecture, no magical light, no halo, no adult Guru Nanak portrait, "
    "no cartoons, no Blender-like plastic figures, no artificial looking faces, "
    "no title cards or text, no duplicated babies or merged anatomy."
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
    job = client.submit(None, PROMPT, 5.0, False, 1470, False, 768, 512, api_name=endpoint)
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
