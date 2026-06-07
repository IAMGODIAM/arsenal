#!/usr/bin/env python3
"""Transcribe all 12 montage clips with word timestamps -> words_full/<clip>.json"""
import sys, json, os, subprocess
from faster_whisper import WhisperModel

CLIPS = ["IMG_0298","IMG_0299","IMG_0312","IMG_0313","IMG_0314","IMG_0316",
         "IMG_0317","IMG_0318","IMG_0319","IMG_0327","IMG_0328","signal_174923"]
SRC = os.path.dirname(__file__) + "/assets/clips"
OUT = os.path.dirname(__file__) + "/words_full"
TMP = "/tmp/wavx"
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)

# small model — better accuracy, we have the RAM+cores
m = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=8)

for c in CLIPS:
    mp4 = f"{SRC}/{c}.mp4"; wav = f"{TMP}/{c}.wav"
    subprocess.run(["ffmpeg","-y","-i",mp4,"-vn","-ac","1","-ar","16000",wav],
                   capture_output=True)
    segs, info = m.transcribe(wav, word_timestamps=True, vad_filter=True, language="en")
    words = []
    for s in segs:
        for w in (s.words or []):
            words.append({"w": w.word.strip(), "s": round(w.start,2), "e": round(w.end,2)})
    json.dump(words, open(f"{OUT}/{c}.json","w"))
    print(f"✓ {c}: {len(words)} words — '{' '.join(x['w'] for x in words)[:90]}...'")
print("DONE")
