#!/usr/bin/env python3
import json, argparse, os, shutil, pathlib, subprocess
P=argparse.ArgumentParser();P.add_argument("--shot",type=int,required=True);a=P.parse_args()
if os.getenv("HF_TOKEN") or os.getenv("RUNWAY_API_KEY") or os.getenv("HEYGEN_API_KEY"):
 raise SystemExit("No paid or authenticated video-generation keys permitted")
HERE=pathlib.Path(__file__).resolve().parent
m=json.loads((HERE/"scenes.json").read_text())
sc=next((s for s in m["scenes"] if s["shot"]==a.shot),None)
if sc is None or sc["reuse_prior_clip"]:raise SystemExit("This shot is reused from an existing verified real model clip")
from gradio_client import Client
client=Client("Lightricks/LTX-2-3",verbose=False)
endpoints=[k for k in client.view_api(return_format="dict").get("named_endpoints",{}) if "generate_video" in k]
if not endpoints:raise SystemExit("Free LTX-2.3 Space has no video endpoint; no fallback")
print("Sending one free genuine moving-video request for scene",a.shot,flush=True)
v=client.submit(None,m["style"]+" "+sc["prompt"],5.0,False,int(sc["seed"]),False,768,512,api_name=endpoints[0]).result(timeout=520)
def path(v):
 if isinstance(v,str) and pathlib.Path(v).is_file():return pathlib.Path(v)
 if isinstance(v,dict):
  if isinstance(v.get("path"),str) and pathlib.Path(v["path"]).is_file():return pathlib.Path(v["path"])
  for x in v.values():
   r=path(x)
   if r:return r
 if isinstance(v,(list,tuple)):
  for x in v:
   r=path(x)
   if r:return r
 return None
source=path(v)
if not source:raise SystemExit("Public video model returned no movie")
out=pathlib.Path("work/clips");out.mkdir(parents=True,exist_ok=True)
dest=out/f"shot_{a.shot:02d}.mp4";shutil.copy2(source,dest)
p=subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration:stream=codec_type","-of","json",str(dest)],text=True)
info=json.loads(p);seconds=float(info["format"]["duration"])
if seconds<4.8 or not any(s["codec_type"]=="video" for s in info.get("streams",[])):raise SystemExit("Invalid motion video:"+p)
print(f"Shot {a.shot} completed, verified {seconds:.3f}s",flush=True)
