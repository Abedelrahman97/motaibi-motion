#!/usr/bin/env python3
"""Contact sheet of a rendered video for review.

Usage: python contact_sheet.py VIDEO OUT.jpg [--every 1.0] [--start 0] [--end END]
One frame every N seconds, 10 per row, timestamp printed on each frame.
"""
import argparse, glob, os, shutil, subprocess, tempfile
from PIL import Image, ImageDraw

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("out")
    ap.add_argument("--every", type=float, default=1.0)
    ap.add_argument("--start", type=float, default=0.0); ap.add_argument("--end", type=float, default=None)
    a = ap.parse_args()
    tmp = tempfile.mkdtemp()
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", str(a.start)]
    if a.end is not None:
        cmd += ["-to", str(a.end)]
    cmd += ["-i", a.video, "-vf", f"fps=1/{a.every},scale=216:-2", os.path.join(tmp, "%04d.jpg")]
    subprocess.run(cmd, check=True)
    fs = sorted(glob.glob(os.path.join(tmp, "*.jpg")))
    if not fs:
        raise SystemExit("no frames")
    w, h = Image.open(fs[0]).size
    cols = 10; rows = (len(fs) + cols - 1) // cols
    sheet = Image.new("RGB", (w * cols, h * rows), "black")
    for i, f in enumerate(fs):
        im = Image.open(f); d = ImageDraw.Draw(im)
        t = a.start + i * a.every
        d.rectangle([0, 0, 64, 22], fill="black"); d.text((4, 4), f"{t:5.1f}s", fill="white")
        sheet.paste(im, ((i % cols) * w, (i // cols) * h))
    sheet.save(a.out, quality=85)
    shutil.rmtree(tmp)
    print(a.out)

if __name__ == "__main__":
    main()
