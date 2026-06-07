#!/usr/bin/env python3
"""FreeKarmelo 3-MIN MASTER — HyperFrames beat-engine. Variable-length testimony, statement captions."""
import json, os, subprocess, re
PROJ=os.path.dirname(os.path.abspath(__file__))+"/master"
SRC=os.path.dirname(os.path.abspath(__file__))+"/../assets/clips"
WORDS=os.path.dirname(os.path.abspath(__file__))+"/../words_full"
W,H=1080,1920
INTRO,OUTRO=8.0,16.0
AUDIO_LEAD=0.35  # J-cut: voice starts before its clip on emotional beats
LEAD_BEATS={'SON','DEF'}

SCRIPT=[
 ("IMG_0313",1.6,5.6,"Karmelo's Mother","ANSWER"),
 ("IMG_0314",1.4,5.4,"Supporter · Collin County","ANSWER"),
 ("IMG_0327",1.6,11.2,"Supporter · Collin County","SON"),
 ("IMG_0318",2.0,22.0,"Supporter · Collin County","SON"),
 ("IMG_0319",7.4,20.8,"Father of a Black Son","DEF"),
 ("IMG_0317",24.0,30.1,"Traveled 1,000+ Miles","DEF"),
 ("IMG_0299",2.2,10.1,"Supporter · Collin County","DEF"),
 ("IMG_0299",20.6,26.1,"Supporter · Collin County","DEF"),
 ("IMG_0328",0.0,11.7,"Community Father · Frisco, TX","STK"),
 ("IMG_0328",18.1,28.0,"Community Father · Frisco, TX","STK"),
 ("IMG_0328",36.4,44.4,"Community Father · Frisco, TX","STK"),
 ("IMG_0328",52.0,63.5,"Community Father · Frisco, TX","STK"),
 ("signal_174923",5.2,30.5,"Supporter · Collin County","INS"),
 ("IMG_0298",3.9,10.4,"Supporter · Collin County","INS"),
 ("IMG_0316",0.0,9.6,"Supporter · Collin County","INS"),
]
HOT=set("karmelo son nephew murder self-defense defense strong god love loved protected brother free justice stay covered head care hear black support truth baby child innocent broken system red ours equal forever odds hands 100%".split())
BEAT_HDR={"ANSWER":"WHY DO YOU SUPPORT KARMELO?","SON":'"HE\'S MY SON"',"DEF":"THIS WAS SELF-DEFENSE","STK":"THE ODDS WERE SET BEFORE HE WALKED IN","INS":"WHAT THEY SAW"}

def norm(w): return re.sub(r'\b(carmel+a|carmell+a|carmel+o|camel+o|camil+l?a|carmil+l?a|graham\s*lowe)\b','Karmelo',w,flags=re.I)
def clean(w): return w.strip().strip('.,?!').lower()
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")
def load_words(clip,ss,ee):
    d=json.load(open(f"{WORDS}/{clip}.json"));out=[]
    for x in d:
        if ss<=x["s"]<ee: out.append({"w":norm(x["w"]),"s":round(x["s"]-ss,3),"e":round(x["e"]-ss,3)})
    return out
def group_lines(words,maxw=5,maxgap=0.45):
    lines,cur=[],[]
    for x in words:
        cur.append(x)
        if len(cur)>=maxw or re.search(r'[.,!?]$',x['w']): lines.append(cur);cur=[]
    if cur: lines.append(cur)
    out=[]
    for ln in lines:
        seg=[ln[0]]
        for w in ln[1:]:
            if w['s']-seg[-1]['e']>maxgap: out.append(seg);seg=[w]
            else: seg.append(w)
        out.append(seg)
    return out

os.makedirs(f"{PROJ}/assets",exist_ok=True)
for (clip,ss,ee,plate,beat) in SCRIPT:
    dur=round(ee-ss,2);tag=f"{clip}_{int(ss*100)}_{int(ee*100)}"
    v=f"{PROJ}/assets/{tag}.mp4";a=f"{PROJ}/assets/{tag}.wav"
    if not os.path.exists(v):
        subprocess.run(["ffmpeg","-y","-ss",str(ss),"-i",f"{SRC}/{clip}.mp4","-t",str(dur),
          "-vf",f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},format=yuv420p","-an","-r","30",v],capture_output=True)
    if not os.path.exists(a):
        subprocess.run(["ffmpeg","-y","-ss",str(ss),"-i",f"{SRC}/{clip}.mp4","-t",str(dur),
          "-vn","-acodec","pcm_s16le","-ar","48000","-ac","2",a],capture_output=True)
print("assets ready")

# ── BUILD LAYOUT ──────────────────────────────────────────────
clip_html,tl_js,cap_idx=[],[],0; last_beat=None; t=INTRO
for idx,(clip,ss,ee,plate,beat) in enumerate(SCRIPT):
    dur=round(ee-ss,2); vdur=round(dur-0.06,2); seg=t; tag=f"{clip}_{int(ss*100)}_{int(ee*100)}"
    if beat!=last_beat:
        bid=f"bh_{beat}_{cap_idx}"
        clip_html.append(f'<div id="{bid}" class="clip" data-start="{seg:.2f}" data-duration="2.6" data-track-index="6" '
            f'style="position:absolute;left:0;right:0;top:200px;text-align:center;padding:0 50px;'
            f'font-family:Georgia,serif;font-weight:700;font-size:40px;color:#E8C84A;text-shadow:0 3px 16px rgba(0,0,0,.95)">{BEAT_HDR[beat]}</div>')
        tl_js.append(f'tl.fromTo("#{bid}",{{opacity:0,y:-18}},{{opacity:1,y:0,duration:.5,ease:"power2.out"}},{seg+.1:.2f}).to("#{bid}",{{opacity:0,duration:.5}},{seg+2.1:.2f});')
        last_beat=beat
    clip_html.append(f'<video class="clip" data-start="{seg:.2f}" data-duration="{vdur:.2f}" data-track-index="0" '
        f'src="assets/{tag}.mp4" muted playsinline style="position:absolute;top:0;left:0;width:{W}px;height:{H}px;object-fit:cover"></video>')
    lead=(AUDIO_LEAD if beat in LEAD_BEATS and idx>0 else 0.0)
    a_start=round(seg-lead,2); a_dur=round(vdur+lead,2)
    clip_html.append(f'<audio data-start="{a_start:.2f}" data-duration="{a_dur:.2f}" data-track-index="1" data-volume="1.0" src="assets/{tag}.wav"></audio>')
    pid=f"pl_{cap_idx}"
    clip_html.append(f'<div id="{pid}" class="clip" data-start="{seg:.2f}" data-duration="{vdur:.2f}" data-track-index="2" '
        f'style="position:absolute;left:48px;top:{H-235}px;font-family:Georgia,serif;font-size:28px;font-weight:700;color:#D4AF37;background:rgba(26,15,46,.92);padding:9px 16px;border-radius:6px;letter-spacing:.5px">{esc(plate)}</div>')
    tl_js.append(f'tl.fromTo("#{pid}",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.5,ease:"power2.out"}},{seg+.15:.2f});')
    for line in group_lines(load_words(clip,ss,ee)):
        l0=line[0]["s"]+seg; l1=min(line[-1]["e"]+seg+0.10, seg+vdur-0.02)
        if l1<=l0: continue
        cid=f"c{cap_idx}"; trk=3+(cap_idx%2); cap_idx+=1; spans=[]
        for j,wd in enumerate(line):
            spans.append(f'<span id="{cid}_w{j}" style="display:inline-block;color:#fff;margin:0 6px">{esc(wd["w"])}</span>')
        clip_html.append(f'<div id="{cid}" class="clip" data-start="{l0:.2f}" data-duration="{(l1-l0):.2f}" data-track-index="{trk}" '
            f'style="position:absolute;left:0;right:0;top:{H-640}px;text-align:center;padding:0 50px;'
            f'font-family:\'Arial Black\',Arial,sans-serif;font-weight:900;font-size:58px;line-height:1.45">'
            f'<span style="background:rgba(8,8,13,.66);padding:10px 22px;border-radius:16px;'
            f'box-decoration-break:clone;-webkit-box-decoration-break:clone;text-shadow:0 3px 12px rgba(0,0,0,.95)">{"".join(spans)}</span></div>')
        tl_js.append(f'tl.fromTo("#{cid}",{{opacity:0,y:24}},{{opacity:1,y:0,duration:.26,ease:"power3.out"}},{l0:.2f});')
        for j,wd in enumerate(line):
            wt=wd["s"]+seg; hot=clean(wd["w"]) in HOT
            col="#E8C84A" if hot else "#FFE9A8"; sc=1.14 if hot else 1.05
            tl_js.append(f'tl.to("#{cid}_w{j}",{{color:"{col}",scale:{sc},duration:.12,ease:"power1.out"}},{wt:.2f}).to("#{cid}_w{j}",{{scale:1,duration:.18,ease:"power1.in"}},{wt+.12:.2f});')
    t=round(t+dur,2)
TOTAL=round(t+OUTRO,2)

hook=f'''<div id="hookcard" class="clip" data-start="0" data-duration="{INTRO:.2f}" data-track-index="7" style="position:absolute;inset:0;background:radial-gradient(circle at 50% 38%,#2A1846 0%,#08080d 78%);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 70px"><div id="hktop" style="font-family:Arial;font-weight:700;font-size:34px;color:#D4AF37;letter-spacing:2px;line-height:1.4;margin-bottom:30px">THEY CAME A THOUSAND MILES<br>FOR A BOY THEY NEVER MET</div><div id="hkbig" style="font-family:'Arial Black',Arial;font-weight:900;font-size:108px;color:#fff;line-height:1.04">WHY?</div><div id="hksub" style="font-family:Arial;font-weight:700;font-size:30px;color:#bbb;letter-spacing:3px;margin-top:34px">ASK EVERY ONE OF THEM</div></div>'''
tl_js.insert(0,f'tl.fromTo("#hktop",{{opacity:0,y:18}},{{opacity:1,y:0,duration:.6,ease:"power2.out"}},.4);')
tl_js.insert(1,f'tl.fromTo("#hkbig",{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:.7,ease:"back.out(1.5)"}},1.2);')
tl_js.insert(2,f'tl.fromTo("#hksub",{{opacity:0}},{{opacity:1,duration:.5}},2.4);')
tl_js.insert(3,f'tl.to("#hookcard",{{opacity:0,duration:.6,ease:"power1.in"}},{INTRO-.6:.2f});')

o=t
outro=f'''<div id="outrocard" class="clip" data-start="{o:.2f}" data-duration="{OUTRO:.2f}" data-track-index="7" style="position:absolute;inset:0;background:radial-gradient(circle at 50% 42%,#2A1846 0%,#08080d 80%);display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 60px"><div id="oa" style="font-family:Arial;font-weight:600;font-size:24px;color:#9a8bb5;line-height:1.5;margin-bottom:44px;max-width:820px">Accounts from supporters present at the Collin County courthouse, June 6 2026. Presumption of innocence applies. The evidence will be decided in court.</div><div id="o1" style="font-family:'Arial Black',Arial;font-weight:900;font-size:62px;color:#E8C84A;line-height:1.1;margin-bottom:24px">THIS WAS<br>SELF-DEFENSE</div><div id="o2" style="font-family:'Arial Black',Arial;font-weight:900;font-size:50px;color:#fff;margin-bottom:30px">FREE KARMELO ANTHONY</div><div id="o3" style="font-family:Arial;font-weight:700;font-size:44px;color:#D4AF37;letter-spacing:1px">freekarmelo.net</div></div>'''
tl_js.append(f'tl.fromTo("#oa",{{opacity:0}},{{opacity:1,duration:.7}},{o+.3:.2f});')
tl_js.append(f'tl.fromTo("#o1",{{opacity:0,y:26}},{{opacity:1,y:0,duration:.6,ease:"power3.out"}},{o+2.2:.2f});')
tl_js.append(f'tl.fromTo("#o2",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.5,ease:"power2.out"}},{o+3.0:.2f});')
tl_js.append(f'tl.fromTo("#o3",{{opacity:0}},{{opacity:1,duration:.5}},{o+3.7:.2f});')

html=f'''<!doctype html><html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width={W}, height={H}"/><script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script><style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#000}}</style></head><body><div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">{hook}
{chr(10).join(clip_html)}
{outro}</div><script>window.__timelines=window.__timelines||{{}};const tl=gsap.timeline({{paused:true}});
{chr(10).join(tl_js)}
window.__timelines["main"]=tl;</script></body></html>'''
open(f"{PROJ}/index.html","w").write(html)
mins=int(TOTAL//60); secs=TOTAL-mins*60
print(f"MASTER: {TOTAL}s ({mins}:{secs:04.1f}) · {len(SCRIPT)} windows · {cap_idx} caption lines")
