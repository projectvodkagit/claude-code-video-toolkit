#!/usr/bin/env python3
"""Local clip-first editor. No network, AI API, publishing, or paid generation."""
from __future__ import annotations
import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def command(parts):
    subprocess.run([str(p) for p in parts], check=True)


def duration(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True)
    return float(result.stdout.strip())


def validate(root, require_assets=False):
    data = json.loads((root / "episode.json").read_text(encoding="utf-8"))
    ledger = json.loads((root / "sources.json").read_text(encoding="utf-8"))
    errors, warnings = [], []
    shots = data.get("shots", [])
    if not shots:
        errors.append("At least one character-led shot is required")
    if data.get("format") not in ("9:16", "16:9"):
        errors.append("Only 9:16 and 16:9 formats are supported")
    if data.get("paid_generation_allowed") is not False:
        errors.append("Paid generation must be explicitly disabled")
    if data.get("requires_human_approval") is not True:
        errors.append("Human approval gate must remain enabled")
    source_ids = {s.get("id") for s in ledger.get("sources", [])}
    claim_ids = {c.get("id") for c in data.get("claims", [])}
    for claim in data.get("claims", []):
        if not claim.get("source_ids") or not set(claim["source_ids"]) <= source_ids:
            errors.append(f"{claim.get('id')}: unsourced claim")
        if claim.get("status") not in (
                "historical_consensus", "traditional_and_scholarly",
                "janamsakhi_tradition", "scriptural_teaching"):
            errors.append(f"{claim.get('id')}: missing evidence classification")
        if claim.get("status") == "janamsakhi_tradition":
            warnings.append(f"{claim.get('id')}: must be described as tradition")
    if len({s.get("id") for s in shots}) != len(shots):
        errors.append("Duplicate shot ID")
    total = 0.0
    for shot in shots:
        name = shot.get("id", "unknown")
        sec = shot.get("duration", 0)
        if not isinstance(sec, (int, float)) or sec <= 0:
            errors.append(f"{name}: duration must be positive")
        else:
            total += sec
        if shot.get("type") not in ("blender", "filmed", "imported_motion"):
            errors.append(f"{name}: static images are forbidden; use acting footage")
        if not shot.get("characters"):
            errors.append(f"{name}: at least one character required")
        if not set(shot.get("claim_ids", [])) <= claim_ids:
            errors.append(f"{name}: unknown historical claim")
        clip = shot.get("clip", "")
        if not (clip.startswith("clips/") and clip.endswith(".mp4")
                and ".." not in clip and "\\" not in clip):
            errors.append(f"{name}: expected clips/<name>.mp4")
            continue
        if require_assets:
            file = root / clip
            if not file.is_file():
                errors.append(f"Missing moving video: {file}")
            elif shutil.which("ffprobe"):
                try:
                    if duration(file) < sec - 0.15:
                        errors.append(f"{name}: clip shorter than shot")
                except Exception as exc:
                    errors.append(f"{name}: invalid MP4: {exc}")
    if abs(total - float(data.get("duration_seconds", -1))) > 0.2:
        errors.append(f"Shots add to {total:.2f}s; target duration differs")
    if require_assets and not (root / "voice.wav").is_file():
        errors.append("Missing narration: voice.wav")
    return data, errors, warnings


def scratch_voice(root, rate=155, name=None):
    if not shutil.which("say"):
        raise RuntimeError("Scratch TTS requires macOS say; alternatively supply voice.wav")
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg not installed")
    script = root / "voice.txt"
    if not script.is_file():
        raise RuntimeError("Missing voice.txt")
    with tempfile.TemporaryDirectory() as tmp:
        aiff = Path(tmp) / "scratch.aiff"
        parts = ["say", "-r", str(rate)]
        if name:
            parts += ["-v", name]
        command(parts + ["-f", script, "-o", aiff])
        command(["ffmpeg", "-y", "-loglevel", "error", "-i", aiff,
                 "-ar", "48000", "-ac", "2", root / "voice.wav"])
    print(f"Scratch voice ready: {root / 'voice.wav'}. Review pronunciation before publishing.")


def render(root, size="540x960", fps=24):
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        raise RuntimeError("Install ffmpeg and ffprobe first")
    episode, errors, warnings = validate(root, True)
    if errors:
        raise RuntimeError("Cannot render:\n - " + "\n - ".join(errors))
    for item in warnings:
        print("REVIEW:", item)
    w, h = (int(x) for x in size.lower().split("x"))
    ratio = 9 / 16 if episode["format"] == "9:16" else 16 / 9
    if w % 2 or h % 2 or abs(w / h - ratio) > 0.012:
        raise ValueError("Output dimensions must be even and match 9:16 or 16:9")
    target = float(episode["duration_seconds"])
    out = root / "output"
    out.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        temp = Path(tmp)
        segments, starts = [], {}
        offset = 0.0
        for i, shot in enumerate(episode["shots"]):
            seconds = float(shot["duration"])
            starts[shot["id"]] = offset
            offset += seconds
            segment = temp / f"segment-{i:03d}.mp4"
            vf = (f"fps={fps},scale={w}:{h}:force_original_aspect_ratio=increase,"
                  f"crop={w}:{h},setsar=1,format=yuv420p")
            command(["ffmpeg", "-y", "-loglevel", "error", "-i", root / shot["clip"],
                     "-t", seconds, "-an", "-vf", vf, "-c:v", "libx264",
                     "-preset", "veryfast", "-crf", "24", segment])
            segments.append(segment)
        listing = temp / "files.txt"
        listing.write_text("".join(f"file '{p}'\n" for p in segments), encoding="utf-8")
        silent = temp / "silent.mp4"
        command(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
                 "-i", listing, "-c:v", "copy", "-an", silent])
        inputs = ["ffmpeg", "-y", "-loglevel", "error", "-i", silent,
                  "-i", root / "voice.wav"]
        audio = [f"[1:a]aresample=48000,apad,atrim=duration={target}[a1]"]
        labels = ["[a1]"]
        index = 2
        music = root / "music.wav"
        if music.is_file():
            inputs += ["-stream_loop", "-1", "-i", music]
            audio += [f"[{index}:a]aresample=48000,atrim=duration={target},volume=0.15[a{index}]"]
            labels += [f"[a{index}]"]
            index += 1
        for shot in episode["shots"]:
            effect = root / "effects" / (shot["id"] + ".wav")
            if effect.is_file():
                inputs += ["-i", effect]
                delay = int(round(starts[shot["id"]] * 1000))
                audio += [f"[{index}:a]aresample=48000,atrim=duration={shot['duration']},"
                          f"adelay={delay}|{delay},volume=0.35[a{index}]"]
                labels += [f"[a{index}]"]
                index += 1
        audio += ["".join(labels) + f"amix=inputs={len(labels)}:"
                  "duration=first:dropout_transition=0,alimiter=limit=0.95[aout]"]
        final = out / "PREVIEW.mp4"
        command(inputs + ["-filter_complex", ";".join(audio), "-map", "0:v:0",
                          "-map", "[aout]", "-t", target, "-c:v", "copy",
                          "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", final])
    print(f"PREVIEW ONLY: {final} ({duration(final):.2f}s). Historical review still required.")
    return final


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    val = sub.add_parser("validate")
    val.add_argument("episode", type=Path)
    val.add_argument("--require-assets", action="store_true")
    speech = sub.add_parser("voice")
    speech.add_argument("episode", type=Path)
    speech.add_argument("--rate", type=int, default=155)
    speech.add_argument("--voice")
    movie = sub.add_parser("render")
    movie.add_argument("episode", type=Path)
    movie.add_argument("--size", default="540x960")
    args = parser.parse_args()
    if args.command == "doctor":
        for program in ("git", "node", "uv", "blender", "ffmpeg", "ffprobe", "say"):
            print(f"{program:10} {shutil.which(program) or 'NOT FOUND'}")
    elif args.command == "validate":
        _, errors, warnings = validate(args.episode, args.require_assets)
        for message in warnings:
            print("REVIEW:", message)
        if errors:
            raise SystemExit("\n".join(errors))
        print("Manifest and source references pass structural validation. Content is NOT historically approved.")
    elif args.command == "voice":
        scratch_voice(args.episode, args.rate, args.voice)
    elif args.command == "render":
        render(args.episode, args.size)


if __name__ == "__main__":
    main()
