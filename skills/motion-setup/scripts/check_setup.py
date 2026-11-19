#!/usr/bin/env python3
"""Check the five tools needed by motaibi-motion and print x/5."""
import shutil, subprocess, sys

def run(cmd):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60,
                           shell=(sys.platform == "win32"))
        return r.returncode == 0, (r.stdout or r.stderr).strip().splitlines()[0] if (r.stdout or r.stderr) else ""
    except Exception as e:  # missing binary, timeout
        return False, str(e)

def node_ok():
    ok, out = run(["node", "--version"])
    if not ok:
        return False, "Node.js not found"
    try:
        major = int(out.lstrip("v").split(".")[0])
    except ValueError:
        return False, out
    return major >= 22, f"{out} (needs 22+)" if major < 22 else out

def whisper_ok():
    try:
        import faster_whisper  # noqa: F401
        return True, "faster-whisper"
    except ImportError:
        return False, "pip install faster-whisper"

def hyperframes_ok():
    if not shutil.which("npx") and not shutil.which("npx.cmd"):
        return False, "npx not found (install Node.js)"
    return run(["npx", "--yes", "hyperframes", "--version"])

checks = [
    ("Node.js 22+", node_ok),
    ("FFmpeg", lambda: run(["ffmpeg", "-version"])),
    ("yt-dlp", lambda: run(["yt-dlp", "--version"])),
    ("Whisper", whisper_ok),
    ("HyperFrames", hyperframes_ok),
]

passed = 0
for name, fn in checks:
    ok, info = fn()
    passed += ok
    print(f"{'✅' if ok else '❌'} {name:<12} {info}")
print(f"\n{passed}/5")
sys.exit(0 if passed == 5 else 1)
