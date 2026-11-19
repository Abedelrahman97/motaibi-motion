---
name: motion-revise
description: Apply the user's change requests to an already-rendered motion montage, changing only the requested part and re-rendering. Use when the user says "غيّر هذا الجزء", "عدّل", "كبّر الكلمة", "بدل الأيقونة", "change this part", or comments on a rendered video.
---

# motion-revise: التعديل

The user writes in plain words. Your job is to change **only** what they asked, keep everything else identical, and show before/after.

## 1. Locate the part
The request may point to a time ("الثانية 12"), a sentence («لما بقول الأدوات»), a chapter («فصل الذوق») or a description («المربع الأخضر الثاني»).
- Map it to the scene row in `build/<name>/plan.md` and to the words in `words.json`.
- If it could match two places, ask one short question with both options and their timestamps.

## 2. Before snapshot
`python ../motion-montage/scripts/contact_sheet.py out/<name>.mp4 build/<name>/before.jpg --start <s-1> --end <e+1> --every 0.25`

## 3. Change it
Common requests and what they mean:
| User says | Do |
|---|---|
| «الكلمة غلط» | fix words.json + caption text, keep timing |
| «كبّر/صغّر» | change size of that element only, re-check it fits the safe area |
| «أسرع/أبطأ» | shift that group's animation timing; never stretch the VO |
| «غيّر اللون» | use another colour **from style.json palette**; if they want a new colour, add it to style.json first |
| «بدّل الأيقونة/الصورة» | use their asset from assets/, or a letter tile; never invent a logo |
| «احذف هذا الجزء» | remove the visual; if they mean the speech too, cut the audio and shift all later timings |

Update plan.md so it stays the source of truth. If the request changes the style for all future videos (e.g. "دايماً خلّي الكابشن أكبر"), also update style.json and say so.

## 4. Re-render and compare
Render, make the after sheet for the same range, Read both, and confirm the change is visible and nothing else moved.
Reply in Arabic: what changed in one line + «تم التعديل ✅». Keep earlier versions as `out/<name>_v1.mp4`, `_v2`… so the user can go back.
