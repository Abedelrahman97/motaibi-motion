---
name: motion-taste
description: Learn the user's visual taste from 2–5 reference videos and write a reusable style guide (style/taste.md + style/style.json) for the montage. Use when the user says "تعلّم ذوقي", "هاي الفيديوهات اللي عجبتني", "learn my style", or drops videos into refs/.
---

# motion-taste: تعلّم الذوق

Output: `style/taste.md` (human-readable, Arabic) and `style/style.json` (machine-readable, used by motion-montage). Nothing is rendered in this step.

## 1. Collect references
- Files in `refs/`, or links the user pastes. For links: `yt-dlp -f "bv*[height<=1920]+ba/b" -o "refs/%(id)s.%(ext)s" URL`.
- References are for **learning style only**. Never reuse their footage, logos, characters, voice or music in the user's video. If the user has not said they may use a link, treat it as reference-only.
- 2 to 5 videos is ideal. If only one, warn that the style will copy that video closely.

## 2. Analyse each video
Run: `python <this skill folder>/scripts/probe_video.py refs/<file> style/probe/<name>`
Then **Read every `sheet_N.jpg`** (they are the video, one frame per second) and `report.json`.
If HyperFrames is installed, `/style-sampling` and `/reverse-any-video` can give a second opinion; use them when available.

Write down, per video:
- **Canvas**: size, background (flat / gradient / texture / grid), safe margins.
- **Palette**: 3–5 hex values from `report.json` and what each is used for (background, text, highlight, cards, lines).
- **Type**: Arabic font family feel (geometric/naskh/rounded), weight, size relative to width, where captions sit.
- **Captions**: words per caption, whether each word is boxed/highlighted, which words get highlight (verbs? nouns? numbers?), entry animation.
- **Rhythm**: `hard_cuts` and `cuts_per_10s`. ≈0 cuts + high `avg_frame_change` = continuous motion graphics. Average caption change interval (count caption changes in the sheets).
- **Visual language**: icon style (flat, outlined, 3D), cards, connectors, progress indicators, chapter labels, how scenes build up (incremental add vs. full replace).
- **Audio**: voice-over only, music bed, SFX on pops (listen if possible; otherwise ask).

## 3. Merge into one taste
Keep what repeats across references; drop one-offs. Where references disagree, ask the user one question with two options.
If the user has brand colours/logo in `assets/`, **brand colours override reference colours**; keep the reference structure.

## 4. Write the files
`style/style.json` keys (fill all):
```json
{
  "canvas": {"w":1080,"h":1920,"fps":30,"bg":"#F1F1E8","texture":"grid","grid_color":"#DEE3D8","grid_px":60,"vignette":true},
  "palette": {"text":"#0F2E2A","highlight":"#1EE08A","card_dark":"#0A3B37","line":"#138E58","card_light":"#FFFFFF"},
  "type": {"arabic":"Tajawal","latin":"Tajawal","caption_px":96,"weight":800},
  "captions": {"position":"top","y_px":330,"max_words":4,"boxed_keywords":true,"box_radius":22,"highlight_rule":"key nouns and verbs","enter":"pop 120ms"},
  "rhythm": {"hard_cuts":false,"caption_change_s":1.0,"scene_build":"incremental"},
  "frame": {"progress_bar":"left-vertical","chapter_pill":"bottom-center","chapters":true},
  "icons": {"style":"flat rounded","source":"simple shapes + real logos from assets only"},
  "audio": {"music":"low bed under VO","sfx":"soft pop on caption"}
}
```
A ready-made preset of the paper-grid explainer style is in `../../styles/paper-grid-explainer.json`; start from it when the references look similar.

`style/taste.md`: 8–12 Arabic bullet points the user can read and correct, e.g. «خلفية ورق مربعات فاتح، الكلمات المهمة داخل مربعات خضراء، ولا يوجد قص حاد».

## 5. Confirm
Show the user taste.md in the chat and ask: «هيك فهمت ذوقك. في شي بدك تغيّره قبل ما نمنتج؟» Apply corrections to both files.
