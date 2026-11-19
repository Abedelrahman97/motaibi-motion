---
name: motion-montage
description: Turn the user's voice-over or talking video into a finished 9:16 Arabic motion-graphics video in their learned style, built with HyperFrames and rendered to MP4. Use when the user says "منتج", "مونتج هذا الفيديو", "اعمل الفيديو", "make the video", or drops files into raw/.
---

# motion-montage: المونتاج

Input: a voice-over (audio or video) in `raw/`, plus `style/style.json`. If style.json is missing, run **motion-taste** first, or (if the user agrees) start from `../../styles/paper-grid-explainer.json`.
Output: `out/<name>.mp4` (1080×1920, 30fps, H.264, AAC) and `out/<name>_sheet.jpg`.

## 1. Transcribe
`python <this skill folder>/scripts/transcribe.py raw/<file> build/<name>/transcript`
Show `transcript.txt` to the user and ask for corrections to names, brands and English words. **Fix words.json with their corrections** (keep the timings) before building anything. Captions with spelling mistakes ruin the video.

## 2. Plan the scenes (show the plan before building)
Write `build/<name>/plan.md` as a table and show it:

| # | from–to (s) | caption words (≤ max_words) | boxed words | chapter | visual |
|---|---|---|---|---|---|

Rules:
- Caption groups follow the speech: break at pauses and at 2–4 words. Each group lasts from its first word's start to the next group's start.
- Box 1–3 meaning-carrying words per group (follow `captions.highlight_rule`). Never box filler words (اللي، بس، وهو، رح).
- Chapters = the logical steps of the script (e.g. التطبيق، الملف، الأدوات، الذوق، المونتاج، التعديل). The chapter pill changes only at chapter boundaries.
- One central visual per chapter that **builds up** as the VO mentions things (`scene_patterns` in the style). Do not replace the whole screen every caption.
- Use only real assets from `assets/` for logos and product images. For third-party tools without a provided logo, use a letter tile (R, H, F, W…), never an invented logo.
- No invented numbers on screen. If the VO says "ملايين", show a rising chart without numbers.

Wait for the user's OK on the plan (or apply their changes).

## 3. Build with HyperFrames
- Work inside `build/video` (created by motion-setup). Use the HyperFrames skills (`/hyperframes`, `/hyperframes-cli`) for the exact composition syntax; do not guess attributes.
- One HTML composition, 1080×1920, duration = audio length + 0.5s. Put the VO as the audio track.
- Background, palette, fonts, caption box style, progress bar and chapter pill come from style.json. Arabic text: `dir="rtl"`, `lang="ar"`, load the Arabic font locally from `assets/fonts` or a Google Fonts link, and keep latin words inside `<bdi>`.
- Timing comes from words.json: every caption group and every visual element is keyed to word start times, so motion lands on the spoken word.
- Animate with short eases (120–250ms). Elements enter with scale 0.9→1 + fade; nothing flies across the screen.
- If the style has music/SFX and the user supplied files in `assets/audio`, mix music around −22 dB under the VO. Never download music.

## 4. Render and self-review
1. `npx hyperframes preview` for the user if they want to watch live.
2. `npx hyperframes render` → move to `out/<name>.mp4`.
3. `python <this skill folder>/scripts/contact_sheet.py out/<name>.mp4 out/<name>_sheet.jpg --every 0.5` and **Read the sheet**. Check: caption spelling, nothing cut off at edges, boxes behind the right words, chapter pill matches, progress bar moves, no empty frames, last frame holds the CTA.
4. Fix and re-render before showing the user.

## 5. Deliver
Give the path to the MP4 and two lines: what was built and one thing the user may want to adjust. Then: «إذا بدك تغيّر أي جزء، اكتبلي الثانية أو الجملة وشو بدك.» (that hands off to motion-revise).
