#!/usr/bin/env python3
"""Offline narration, original ambient score, caption burn and final 45s video."""
from pathlib import Path
import subprocess, shutil, argparse

P=Path(__file__).resolve().parent
def run(*cmd):
    print("+"," ".join(str(x) for x in cmd),flush=True)
    subprocess.run([str(x) for x in cmd],check=True)
p=argparse.ArgumentParser()
p.add_argument("--input",default="build/birth1469_silent.mp4")
p.add_argument("--output",default="build/guru_nanak_birth_1469_reel.mp4")
p.add_argument("--voice",default="")
args=p.parse_args()
video=Path(args.input)
out=Path(args.output)
out.parent.mkdir(parents=True,exist_ok=True)
if not video.is_file():raise SystemExit("Missing real 3D render: "+str(video))
if not shutil.which("ffmpeg"):raise SystemExit("ffmpeg required")
voice=Path(args.voice) if args.voice else out.parent/"voice.wav"
if not voice.is_file():
    if not shutil.which("espeak-ng") and not shutil.which("espeak"):
        raise SystemExit("Install espeak-ng or provide --voice path/to/voice.wav")
    tts=shutil.which("espeak-ng") or shutil.which("espeak")
    run(tts,"-v","en-us","-s","146","-p","42","-a","175",
        "-f",P/"narration.txt","-w",voice)
# Unlicensed recordings and music are excluded. All generated music is synthesised original tones.
# Voice begins 1.2s in, with enough space for a closing beat.
ass=P/"captions.ass"
if not ass.exists():raise SystemExit("Missing caption file")
# Constrain voice to 42s to keep total exactly 45 s, retain pitch.
# Mix a restrained original warm ambient bed (sine waves) and subtle wind.
video_input=[
 "ffmpeg","-y","-hide_banner","-loglevel","error","-i",video,"-i",voice,
 "-f","lavfi","-i","sine=frequency=146.83:sample_rate=44100:duration=45",
 "-f","lavfi","-i","sine=frequency=220:sample_rate=44100:duration=45",
 "-f","lavfi","-i","anoisesrc=color=brown:amplitude=0.16:sample_rate=44100:duration=45"
]
flt=(
 "[1:a]aresample=44100,atrim=duration=42,adelay=1200|1200,"
 "highpass=f=130,acompressor=threshold=-28dB:ratio=2.5:attack=8:release=160,"
 "volume=1.35[v];"
 "[2:a]volume=0.026,afade=t=in:st=0:d=3,afade=t=out:st=41:d=4[m1];"
 "[3:a]volume=0.012,afade=t=in:st=3:d=8,afade=t=out:st=41:d=4[m2];"
 "[4:a]lowpass=f=500,volume=0.04,afade=t=in:st=0:d=3,"
 "afade=t=out:st=41:d=4[amb];"
 "[v][m1][m2][amb]amix=inputs=4:duration=longest:dropout_transition=0,"
 "alimiter=limit=0.94[a]"
)
run(*(video_input+[
 "-filter_complex",flt,"-filter_threads","1","-map","0:v:0","-map","[a]",
 "-vf","ass="+str(ass)," -unused-option-not-real" if False else "-t","45",
 "-c:v","libx264","-preset","veryfast","-crf","19","-pix_fmt","yuv420p",
 "-r","30","-c:a","aac","-b:a","192k","-movflags","+faststart",out
]))
print("FINISHED",out,flush=True)
