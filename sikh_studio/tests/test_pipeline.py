"""Offline tests only: generated test pattern is NOT historical footage."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pipeline import validate, render


class StudioTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        (self.root / "clips").mkdir()
        (self.root / "sources.json").write_text(json.dumps({"sources":[{"id":"S1"}]}))
        self.episode = {
            "id":"smoke", "format":"9:16", "duration_seconds":2.0,
            "paid_generation_allowed":False,"requires_human_approval":True,
            "claims":[{"id":"C1","status":"historical_consensus","source_ids":["S1"]}],
            "shots":[{"id":"01","duration":2,"type":"blender","characters":["actor"],
                      "clip":"clips/01.mp4","claim_ids":["C1"]}]
        }
        self.save()

    def save(self):
        (self.root / "episode.json").write_text(json.dumps(self.episode))

    def test_valid_storyboard(self):
        self.assertEqual(validate(self.root)[1], [])

    def test_missing_clip_rejected(self):
        self.assertTrue(any("Missing moving video" in e for e in validate(self.root, True)[1]))

    def test_still_images_rejected(self):
        self.episode["shots"][0]["type"] = "still"
        self.save()
        self.assertTrue(any("static images" in e for e in validate(self.root)[1]))

    def test_paid_generation_and_unsourced_claims_rejected(self):
        self.episode["paid_generation_allowed"] = True
        self.episode["claims"][0]["source_ids"] = ["not-a-source"]
        self.save()
        errs = validate(self.root)[1]
        self.assertTrue(any("Paid generation" in e for e in errs))
        self.assertTrue(any("unsourced" in e for e in errs))

    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "ffmpeg unavailable")
    def test_moving_video_and_audio_export(self):
        clip = self.root / "clips/01.mp4"
        subprocess.run(["ffmpeg","-y","-loglevel","error","-f","lavfi","-i",
                        "testsrc2=size=180x320:rate=24:duration=2.3",
                        "-c:v","libx264","-pix_fmt","yuv420p",str(clip)], check=True)
        subprocess.run(["ffmpeg","-y","-loglevel","error","-f","lavfi","-i",
                        "sine=frequency=220:sample_rate=48000:duration=2.3",
                        "-ac","2",str(self.root / "voice.wav")],check=True)
        result = render(self.root, "180x320")
        self.assertTrue(result.exists())
        self.assertGreater(result.stat().st_size, 9000)


if __name__ == "__main__":
    unittest.main()
