#!/usr/bin/env python3
"""Word-timed transcription for montage.

Usage: python transcribe.py AUDIO_OR_VIDEO OUT_DIR [--model small] [--lang ar]

Writes OUT_DIR/words.json  [{"w": word, "s": start, "e": end}, ...]
       OUT_DIR/segments.json  [{"text":..., "s":..., "e":...}]
       OUT_DIR/transcript.txt  plain text for the user to correct
"""
import argparse, json, os, subprocess, tempfile

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("out")
    ap.add_argument("--model", default="small"); ap.add_argument("--lang", default="ar")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    wav = os.path.join(tempfile.gettempdir(), "mm_audio.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", a.src, "-ac", "1", "-ar", "16000", wav], check=True)

    from faster_whisper import WhisperModel
    model = WhisperModel(a.model, device="auto", compute_type="int8")
    segs, _ = model.transcribe(wav, language=a.lang, word_timestamps=True, vad_filter=True)

    words, segments = [], []
    for s in segs:
        segments.append({"text": s.text.strip(), "s": round(s.start, 2), "e": round(s.end, 2)})
        for w in s.words or []:
            words.append({"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)})

    with open(os.path.join(a.out, "words.json"), "w", encoding="utf-8") as f:
        json.dump(words, f, ensure_ascii=False, indent=1)
    with open(os.path.join(a.out, "segments.json"), "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=1)
    with open(os.path.join(a.out, "transcript.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(s["text"] for s in segments))
    print(f"{len(words)} words, {len(segments)} segments -> {a.out}")

if __name__ == "__main__":
    main()
