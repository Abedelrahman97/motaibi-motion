---
name: motion-setup
description: Install and verify the five tools needed for Arabic motion-graphics montage (Node.js 22+, FFmpeg, yt-dlp, Whisper, HyperFrames) and prepare the project folder. Use when the user says "ثبّت الأدوات", "جهّز الجهاز", "setup", or before the first montage on a new machine.
---

# motion-setup: تجهيز الأدوات

The goal is a working project folder where `scripts/check_setup.py` prints **5/5**. Talk to the user in Arabic, briefly, and show progress as `n/5`.

## 1. Detect the system first
Run `python --version` (or `python3`), `node --version`, `ffmpeg -version`, `yt-dlp --version`.
Decide the package manager: Windows → `winget`, macOS → `brew`, Linux → `apt`. Never guess; check what exists.

## 2. Install only what is missing
| # | Tool | Why | Windows | macOS |
|---|------|-----|---------|-------|
| 1 | Node.js 22+ | runs HyperFrames | `winget install OpenJS.NodeJS.LTS` | `brew install node` |
| 2 | FFmpeg | cut, encode, audio | `winget install Gyan.FFmpeg` | `brew install ffmpeg` |
| 3 | yt-dlp | download reference videos the user has the right to use | `winget install yt-dlp.yt-dlp` | `brew install yt-dlp` |
| 4 | Whisper | word-timed Arabic transcription | `pip install faster-whisper pillow numpy` | same |
| 5 | HyperFrames | writes the video as HTML and renders MP4 | `npx hyperframes skills update` | same |

Notes:
- After installing FFmpeg or Node on Windows, tell the user to **close and reopen the terminal** (PATH refresh), then continue.
- HyperFrames ships its own Claude Code skills (`/hyperframes`, `/hyperframes-cli`, `/style-sampling`, `/reverse-any-video`, `/media-use`). They are the reference for composition syntax; this plugin decides *what* to build, HyperFrames skills decide *how* to write it.
- Remotion is optional. Do not install it unless the user asks.

## 3. Create the project folder
In the folder the user opened Claude Code in, create:
```
my-montage/
  refs/        reference videos the user likes (taste)
  raw/         the user's own footage / voice-over
  assets/      logo, product photos, fonts
  style/       taste.md + style.json (written by motion-taste)
  build/       HyperFrames project and renders
  out/         final MP4s
```
Then run `npx hyperframes init build/video` (inside `my-montage`).

## 4. Verify
Run `python <this skill folder>/scripts/check_setup.py`. It prints each tool and `x/5`.
Only say "جاهز" when it prints 5/5. If one fails, fix that one and re-run; do not reinstall everything.

## 5. Hand-off message (Arabic)
"✅ الأدوات جاهزة 5/5. الخطوة التالية: حط 2 إلى 5 فيديوهات عاجبتك بمجلد refs واكتب: «تعلّم ذوقي»."
