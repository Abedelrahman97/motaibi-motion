#!/usr/bin/env python3
"""Analyse a reference video for style learning.

Usage: python probe_video.py VIDEO OUT_DIR [--fps 1]

Writes to OUT_DIR:
  frames/NNN.jpg      one frame per 1/fps seconds (270px wide)
  sheet_N.jpg         contact sheets of 10 frames each (read these to see the video)
  report.json         duration, size, fps, hard cuts, cuts per 10s, palette, motion level
"""
import json, os, re, subprocess, sys, glob, argparse
from PIL import Image

def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)

def probe(video):
    r = sh(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
            "stream=width,height,r_frame_rate:format=duration", "-of", "json", video])
    j = json.loads(r.stdout)
    s = j["streams"][0]
    num, den = s["r_frame_rate"].split("/")
    return {"width": s["width"], "height": s["height"],
            "fps": round(int(num) / int(den), 2), "duration": round(float(j["format"]["duration"]), 2)}

def frames(video, out, fps):
    d = os.path.join(out, "frames"); os.makedirs(d, exist_ok=True)
    sh(["ffmpeg", "-v", "error", "-y", "-i", video, "-vf", f"fps={fps},scale=270:-2", os.path.join(d, "%03d.jpg")])
    return sorted(glob.glob(os.path.join(d, "*.jpg")))

def sheets(files, out, per=10):
    paths = []
    for k in range(0, len(files), per):
        ims = [Image.open(f) for f in files[k:k + per]]
        w, h = ims[0].size
        g = Image.new("RGB", (w * len(ims), h), "black")
        for i, im in enumerate(ims):
            g.paste(im, (i * w, 0))
        p = os.path.join(out, f"sheet_{k // per + 1}.jpg"); g.save(p, quality=85); paths.append(p)
    return paths

def cuts(video, thr=0.3):
    r = sh(["ffmpeg", "-v", "info", "-i", video, "-vf", f"select='gt(scene,{thr})',showinfo", "-f", "null", "-"])
    return [round(float(t), 2) for t in re.findall(r"pts_time:([0-9.]+)", r.stderr)]

def palette(files, n=8):
    sample = [Image.open(f).convert("RGB") for f in files[:: max(1, len(files) // 12)]]
    w, h = sample[0].size
    strip = Image.new("RGB", (w * len(sample), h))
    for i, im in enumerate(sample):
        strip.paste(im, (i * w, 0))
    q = strip.quantize(n).convert("RGB")
    total = w * len(sample) * h
    cols = sorted(q.getcolors(total), reverse=True)
    return [{"hex": "#%02x%02x%02x" % c, "share": round(cnt / total, 3)} for cnt, c in cols]

def accents(files, n=5):
    """Saturated colours (highlights, cards, lines) that the background hides in the main palette."""
    import colorsys
    from collections import Counter
    cnt = Counter()
    for f in files[:: max(1, len(files) // 20)]:
        im = Image.open(f).convert("RGB").resize((90, 160))
        import numpy as np
        for r, g, b in np.asarray(im).reshape(-1, 3).tolist():
            h, l, s = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
            if s > 0.35 and 0.12 < l < 0.85:
                cnt[(r // 16 * 16, g // 16 * 16, b // 16 * 16)] += 1
    total = sum(cnt.values()) or 1
    return [{"hex": "#%02x%02x%02x" % c, "share_of_accents": round(k / total, 3)} for c, k in cnt.most_common(n)]

def motion_level(files):
    import numpy as np
    diffs = []
    prev = None
    for f in files:
        a = np.asarray(Image.open(f).convert("L"), dtype=float)
        if prev is not None and a.shape == prev.shape:
            diffs.append(float(abs(a - prev).mean()))
        prev = a
    return round(sum(diffs) / len(diffs), 2) if diffs else 0.0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("out"); ap.add_argument("--fps", type=float, default=1)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    info = probe(a.video)
    fs = frames(a.video, a.out, a.fps)
    c = cuts(a.video)
    rep = {**info, "frames": len(fs), "sheets": sheets(fs, a.out),
           "hard_cuts": c, "cuts_per_10s": round(len(c) / info["duration"] * 10, 2),
           "palette": palette(fs), "accents": accents(fs), "avg_frame_change": motion_level(fs),
           "hint": "hard_cuts≈0 with high avg_frame_change means continuous motion graphics, not cut-based editing"}
    with open(os.path.join(a.out, "report.json"), "w", encoding="utf-8") as f:
        json.dump(rep, f, ensure_ascii=False, indent=2)
    print(json.dumps({k: v for k, v in rep.items() if k != "sheets"}, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
