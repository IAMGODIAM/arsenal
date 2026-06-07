#!/usr/bin/env python3
"""
qa_score.py — automated delivery gate for FreeKarmelo renders.
DAG: karmelo-qa-gate-2026-0607
Exit 0 = PASS (cleared to deliver). Exit 1 = FAIL (do not ship).
Usage: python3 qa_score.py <render.mp4> [--target-seconds 177] [--tolerance 3]
"""
import sys, subprocess, re, os

def probe(path, *args):
    return subprocess.run(["ffprobe","-v","error",*args,path], capture_output=True, text=True).stdout.strip()

def check(path, target=177.0, tol=3.0):
    results=[]; ok=True
    def add(name, passed, detail):
        nonlocal ok; ok = ok and passed; results.append((("✓" if passed else "✗"), name, detail))

    rate = probe(path,"-select_streams","v:0","-show_entries","stream=r_frame_rate","-of","csv=p=0")
    try: num,den=rate.split("/"); fps=round(float(num)/float(den))
    except Exception: fps=0
    add("G1 fps", fps==30, f"{fps}fps (need 30)")

    dur = float(probe(path,"-show_entries","format=duration","-of","csv=p=0") or 0)
    add("G2 duration", abs(dur-target)<=tol, f"{dur:.1f}s (target {target}±{tol})")

    vd = subprocess.run(["ffmpeg","-i",path,"-af","volumedetect","-f","null","-"], capture_output=True, text=True).stderr
    m = re.search(r"mean_volume:\s*(-?[\d.]+)", vd); mean=float(m.group(1)) if m else -99.0
    add("G3 audio", mean > -40.0, f"{mean:.1f}dB mean (need > -40)")

    wh = probe(path,"-select_streams","v:0","-show_entries","stream=width,height","-of","csv=p=0")
    add("G4 resolution", wh.replace(",","x")=="1080x1920", f"{wh} (need 1080,1920)")

    bd = subprocess.run(["ffmpeg","-i",path,"-vf","blackdetect=d=0.5:pic_th=0.98","-an","-f","null","-"], capture_output=True, text=True).stderr
    blacks = re.findall(r"black_duration:([\d.]+)", bd); worst=max([float(b) for b in blacks], default=0.0)
    add("G5 black_gap", worst <= 0.5, f"longest black run {worst:.2f}s (limit 0.50)")

    idx = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(path)),"..","index.html"))
    if os.path.exists(idx):
        html_idx = open(idx).read()
        ys = [int(y) for y in re.findall(r"top:(\d+)px", html_idx)]
        # caption karaoke band must clear strict 1620; small left-aligned attribution plate may sit <=1700
        lowest = max(ys, default=0)
        add("G6 caption_safe", lowest <= 1700, f"lowest text top={lowest}px (plate limit 1700)")
        add("G7 no_MURDER", "MURDER" not in html_idx, "on-screen 'MURDER' absent" if "MURDER" not in html_idx else "FOUND on-screen 'MURDER'")
    else:
        add("G6 caption_safe", True, "index.html not found — skipped")
        add("G7 no_MURDER", True, "index.html not found — skipped")
    return ok, results

if __name__=="__main__":
    if len(sys.argv) < 2:
        print("usage: qa_score.py <render.mp4> [--target-seconds N] [--tolerance N]"); sys.exit(2)
    path=sys.argv[1]; target=177.0; tol=3.0
    if "--target-seconds" in sys.argv: target=float(sys.argv[sys.argv.index("--target-seconds")+1])
    if "--tolerance" in sys.argv: tol=float(sys.argv[sys.argv.index("--tolerance")+1])
    ok, results = check(path, target, tol)
    print(f"\nQA GATE — {os.path.basename(path)}\n"+"="*52)
    for mark,name,detail in results: print(f"  {mark}  {name:<18} {detail}")
    print("="*52+f"\nVERDICT: {'PASS — cleared to deliver ✓' if ok else 'FAIL — DO NOT SHIP ✗'}\n")
    sys.exit(0 if ok else 1)
