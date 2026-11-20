#!/usr/bin/env python3
"""Combine 9 genuine moving clips with exactly matching spoken captions."""
import json, pathlib, subprocess
ROOT=pathlib.Path(__file__).resolve().parent
W=pathlib.Path("work"); O=pathlib.Path("out"); O.mkdir(exist_ok=True)
scenes=json.loads((ROOT/"scenes.json").read_text())["scenes"]
assert len(scenes)==9 and [s["shot"] for s in scenes]==list(range(1,10))
def run(*args):
 print("+"," ".join(str(x) for x in args),flush=True)
 subprocess.run([str(x) for x in args],check=True)
def info(path):
 return json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration,size:stream=codec_type,width,height","-of","json",str(path)],text=True))
def tt(sec):
 n=round(sec*100);h,n=divmod(n,360000);m,n=divmod(n,6000);s,c=divmod(n,100)
 return f"{h}:{m:02d}:{s:02d}.{c:02d}"
ass=["[Script Info]","Title: Verbatim voiceover only","ScriptType: v4.00+","PlayResX: 720","PlayResY: 1280","ScaledBorderAndShadow: yes",
"[V4+ Styles]","Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
"Style: Spoken,DejaVu Sans,38,&H00F9F5EA,&H00F9F5EA,&H00201C16,&H880B0C0D,1,0,0,0,100,100,0,0,1,3,1,2,50,50,140,1",
"[Events]","Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
segments=[]; voices=[]; report=[]
for shot in scenes:
 i=shot["shot"];t=(i-1)*5;words=shot["narration"].split()
 middle=max(3,min(len(words)-3,round(len(words)/2)))
 a,b=" ".join(words[:middle])," ".join(words[middle:])
 assert a+" "+b==shot["narration"]
 for start,end,text in ((t+.2,t+2.42,a),(t+2.42,t+4.9,b)):
  ass.append(f"Dialogue: 0,{tt(start)},{tt(end)},Spoken,,0,0,0,,{text}")
 movie=W/"clips"/f"shot_{i:02d}.mp4"
 if not movie.is_file():raise SystemExit(f"Missing genuinely generated moving clip {i}: {movie}")
 d=info(movie);length=float(d["format"]["duration"])
 if length<4.8 or not any(x["codec_type"]=="video" for x in d["streams"]):
  raise SystemExit(f"Invalid source shot {i}: {length}")
 clip=O/f"cut_{i:02d}.mp4"
 run("ffmpeg","-y","-hide_banner","-loglevel","error","-i",movie,"-t","5","-an",
     "-vf","fps=24,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280,setsar=1,format=yuv420p",
     "-c:v","libx264","-preset","veryfast","-crf","22",clip)
 segments.append(clip)
 wave=W/"audio"/f"voice_{i:02d}.wav"
 if not wave.is_file():raise SystemExit(f"Missing natural voice {i}")
 length_voice=float(info(wave)["format"]["duration"])
 tempo=max(1,length_voice/4.6)
 if tempo>1.45:raise SystemExit(f"Voice {i} too long: {length_voice:.2f}s; edit copy")
 voice=O/f"voice_{i:02d}.wav"
 run("ffmpeg","-y","-hide_banner","-loglevel","error","-i",wave,
     "-filter:a",f"atempo={tempo:.4f},aresample=48000,adelay=170|170,apad,atrim=duration=5",
     "-ac","2","-ar","48000",voice)
 voices.append(voice)
 report.append({"shot":i,"clip_length":length,"voice_length":length_voice,"tempo":tempo})
subs=O/"voiceover_only.ass";subs.write_text("\n".join(ass)+"\n")
listing=O/"clips.txt";listing.write_text("".join(f"file '{p.resolve()}'\n" for p in segments))
silent=O/"picture_45sec.mp4"
run("ffmpeg","-y","-hide_banner","-loglevel","error","-f","concat","-safe","0",
    "-i",listing,"-c:v","copy","-an",silent)
voiceargs=[]
for p in voices:voiceargs.extend(["-i",p])
join="".join(f"[{k}:a]" for k in range(9))+"concat=n=9:v=0:a=1[v]"
whole=O/"spoken_narration.wav"
run("ffmpeg","-y","-hide_banner","-loglevel","error",*voiceargs,
    "-filter_complex",join,"-map","[v]","-ar","48000","-ac","2",whole)
mix=("[1:a]highpass=f=95,acompressor=threshold=-22dB:ratio=2:attack=10:release=165,volume=1.10[vo];"
     "[2:a]lowpass=f=500,volume=0.020,afade=t=in:st=0:d=1,afade=t=out:st=43:d=2[amb];"
     "[vo][amb]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.94,"
     "loudnorm=I=-17:TP=-1.5:LRA=9[a]")
output=O/"guru_nanak_birth_full_45s.mp4"
run("ffmpeg","-y","-hide_banner","-loglevel","error","-i",silent,"-i",whole,
    "-f","lavfi","-i","anoisesrc=color=brown:amplitude=0.04:sample_rate=48000:duration=45",
    "-filter_complex",mix,"-map","0:v:0","-map","[a]",
    "-vf",f"ass={subs.resolve()},eq=contrast=1.025:saturation=1.02",
    "-t","45","-c:v","libx264","-preset","veryfast","-crf","19",
    "-pix_fmt","yuv420p","-r","24","-c:a","aac","-b:a","192k",
    "-movflags","+faststart",output)
final=info(output);dur=float(final["format"]["duration"])
types={x["codec_type"] for x in final["streams"]}
if not (44.8<=dur<=45.2 and {"audio","video"}<=types):
 raise SystemExit(f"Export QA failed: {dur}, {types}")
shots=O/"review_frames";shots.mkdir(exist_ok=True)
for i in range(9):
 run("ffmpeg","-y","-hide_banner","-loglevel","error","-ss",str(i*5+2.5),
     "-i",output,"-frames:v","1","-vf","scale=240:427",shots/f"{i+1:02d}.jpg")
(O/"QA.json").write_text(json.dumps({"status":"draft_for_human_visual_review",
    "duration_seconds":dur,"tracks":sorted(types),"caption_policy":"ONLY exact spoken voiceover fragments",
    "historical_status":"Visual reconstruction, not documentary footage",
    "voice_engine":"offline Kokoro","scenes":report},indent=2)+"\n")
print("READY FOR REVIEW",output,dur,flush=True)
