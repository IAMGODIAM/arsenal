#!/usr/bin/env python3
"""FreeKarmelo FULL MONTAGE — HyperFrames. 12 testimonies in 6 beats + hook/outro cards.
Each clip cropped to vertical 1080x1920, muted video + separate audio track, karaoke captions
(gold pop on hot words), gold nameplate. Strict HyperFrames render path — no ffmpeg compositing."""
import json, os, subprocess, re
PROJ = os.path.dirname(__file__) + "/montage"
SRC  = os.path.dirname(__file__) + "/../assets/clips"
WORDS= os.path.dirname(__file__) + "/../words_full"
W, H = 1080, 1920

# (clip, in_s, dur_s, nameplate, beat-tag) — strongest window per testimony
SEGS = [
    ("IMG_0313", 0.0, 5.6, "Supporter · Collin County",  "SON"),   # "my son, I stand behind him 100%"
    ("IMG_0314", 0.0, 5.4, "Supporter · Collin County",  "SON"),   # "my nephew. Free Karmelo"
    ("IMG_0327", 0.4, 6.8, "Supporter · Collin County",  "SON"),   # "I look at him as if that is my son"
    ("IMG_0318", 0.0, 8.0, "Supporter · Collin County",  "SON"),   # "he's my son, he's my nephew... system is broken"
    ("IMG_0319",10.6, 8.9, "Supporter · Collin County",  "DEF"),   # "this does not mean murder, hands off... stay strong"
    ("IMG_0317", 0.0, 8.0, "Supporter · Collin County",  "DEF"),   # "came a thousand plus... self-defense is not murder" (use end line too)
    ("IMG_0299", 2.4, 8.0, "Supporter · Collin County",  "DEF"),   # "good young brother, 3.7 GPA, not selling dope"
    ("IMG_0328",18.1, 9.9, "Community Father · Frisco, TX","STK"),  # "Collin County is red... odds are against you"
    ("signal_174923", 5.2, 6.1, "Supporter · Collin County","INS"),# "he's one of ours... if the shoe was on the other foot"
    ("IMG_0298", 3.9, 6.5, "Supporter · Collin County",  "INS"),   # "a black kid that needs to be protected, loved, covered by God"
    ("IMG_0316", 0.0, 9.6, "Supporter · Collin County",  "INS"),   # "innocent young brother... the truth will be out, he'll be free"
]
INTRO, OUTRO = 5.5, 5.0
HOT = {"karmelo","son","nephew","murder","self-defense","defense","strong","god","love","loved",
       "protected","brother","free","justice","stay","covered","head","care","hear","black","support",
       "truth","baby","child","innocent","broken","system","red","ours","equal","murder.","murder,"}

def norm(w):
    # normalize all whisper spellings of the name -> Karmelo
    return re.sub(r'\b(carmel+a|carmell+a|carmel+o|camel+o|camil+l?a|carmil+l?a|graham\s*lowe)\b',
                  'Karmelo', w, flags=re.I)
def clean(w): return w.strip().strip('.,?!').lower()
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def load_words(clip, ss, dur):
    d = json.load(open(f"{WORDS}/{clip}.json"))
    out=[]
    for x in d:
        if ss <= x["s"] < ss+dur:
            out.append({"w": norm(x["w"]), "s": round(x["s"]-ss,3), "e": round(x["e"]-ss,3)})
    return out
def group_lines(words, maxw=5, maxgap=0.45):
    lines, cur = [], []
    for x in words:
        cur.append(x)
        ends_phrase = bool(re.search(r'[.,!?]$', x['w']))
        nxtgap_break = False
        if cur and (len(cur)>=maxw or ends_phrase):
            lines.append(cur); cur=[]
            continue
    if cur: lines.append(cur)
    # second pass: split on big pauses within a line
    out=[]
    for ln in lines:
        seg=[ln[0]]
        for w in ln[1:]:
            if w['s']-seg[-1]['e']>maxgap: out.append(seg); seg=[w]
            else: seg.append(w)
        out.append(seg)
    return out

os.makedirs(f"{PROJ}/assets", exist_ok=True)
# pre-crop every clip to vertical 1080x1920 + extract trimmed audio
for (clip, ss, dur, plate, beat) in SEGS:
    vout=f"{PROJ}/assets/{clip}_{int(ss*100)}.mp4"; aout=f"{PROJ}/assets/{clip}_{int(ss*100)}.wav"
    if not os.path.exists(vout):
        subprocess.run(["ffmpeg","-y","-ss",str(ss),"-i",f"{SRC}/{clip}.mp4","-t",str(dur),
            "-vf",f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},format=yuv420p",
            "-an","-r","30",vout],capture_output=True)
    if not os.path.exists(aout):
        subprocess.run(["ffmpeg","-y","-ss",str(ss),"-i",f"{SRC}/{clip}.mp4","-t",str(dur),
            "-vn","-acodec","pcm_s16le","-ar","48000","-ac","2",aout],capture_output=True)

BEAT_HDR = {"SON":"\"HE'S MY SON\"", "DEF":"SELF-DEFENSE IS NOT MURDER",
            "STK":"THE ODDS WERE SET BEFORE HE WALKED IN", "INS":"WHAT THEY SAW INSIDE"}

t=INTRO; clip_html, tl_js, cap_idx=[],[],0; last_beat=None
for (clip, ss, dur, plate, beat) in SEGS:
    seg=t; aid=f"{clip}_{int(ss*100)}"
    # beat header card (brief gold lower-third when beat changes)
    if beat!=last_beat:
        bid=f"beat_{beat}_{cap_idx}"
        clip_html.append(f'<div id="{bid}" class="clip" data-start="{seg:.2f}" data-duration="2.4" data-track-index="6" '
            f'style="position:absolute;left:0;right:0;top:210px;text-align:center;padding:0 50px;'
            f'font-family:Georgia,serif;font-weight:700;font-size:38px;color:#E8C84A;'
            f'text-shadow:0 3px 14px rgba(0,0,0,.95)">{BEAT_HDR[beat]}</div>')
        tl_js.append(f'tl.fromTo("#{bid}",{{opacity:0,y:-18}},{{opacity:1,y:0,duration:.5,ease:"power2.out"}},{seg+.1:.2f}).to("#{bid}",{{opacity:0,duration:.5}},{seg+1.9:.2f});')
        last_beat=beat
    vdur=round(dur-0.06,2)
    clip_html.append(f'<video class="clip" data-start="{seg:.2f}" data-duration="{vdur:.2f}" data-track-index="0" '
        f'src="assets/{aid}.mp4" muted playsinline style="position:absolute;top:0;left:0;width:{W}px;height:{H}px;object-fit:cover"></video>')
    clip_html.append(f'<audio data-start="{seg:.2f}" data-duration="{vdur:.2f}" data-track-index="1" data-volume="1.0" src="assets/{aid}.wav"></audio>')
    pid=f"plate_{cap_idx}"
    clip_html.append(f'<div id="{pid}" class="clip" data-start="{seg:.2f}" data-duration="{vdur:.2f}" data-track-index="2" '
        f'style="position:absolute;left:48px;top:{H-150}px;font-family:Georgia,serif;font-size:28px;font-weight:700;'
        f'color:#D4AF37;background:rgba(26,15,46,.92);padding:9px 16px;border-radius:6px;letter-spacing:.5px">{esc(plate)}</div>')
    tl_js.append(f'tl.fromTo("#{pid}",{{opacity:0,x:-30}},{{opacity:1,x:0,duration:.5,ease:"power2.out"}},{seg+.15:.2f});')
    for line in group_lines(load_words(clip, ss, dur)):
        l0=line[0]["s"]+seg; l1=min(line[-1]["e"]+seg+0.10, seg+vdur-0.02)
        cid=f"cap{cap_idx}"; trk=3+(cap_idx%2); cap_idx+=1; spans=[]
        for j,wd in enumerate(line):
            spans.append(f'<span id="{cid}_w{j}" style="display:inline-block;color:#fff;margin:0 6px">{esc(wd["w"])}</span>')
        cap_html=("".join(spans))
        clip_html.append(
            f'<div id="{cid}" class="clip" data-start="{l0:.2f}" data-duration="{(l1-l0):.2f}" data-track-index="{trk}" '
            f'style="position:absolute;left:0;right:0;top:{H-560}px;text-align:center;padding:0 50px;'
            f'font-family:\'Arial Black\',Arial,sans-serif;font-weight:900;font-size:58px;line-height:1.45">'
            f'<span style="background:rgba(8,8,13,.66);padding:10px 22px;border-radius:16px;'
            f'box-decoration-break:clone;-webkit-box-decoration-break:clone;'
            f'text-shadow:0 3px 12px rgba(0,0,0,.95)">{cap_html}</span></div>')
        tl_js.append(f'tl.fromTo("#{cid}",{{opacity:0,y:26}},{{opacity:1,y:0,duration:.26,ease:"power3.out"}},{l0:.2f});')
        for j,wd in enumerate(line):
            wt=wd["s"]+seg; hot=clean(wd["w"]) in HOT
            col="#E8C84A" if hot else "#FFE9A8"; sc=1.15 if hot else 1.05
            tl_js.append(f'tl.to("#{cid}_w{j}",{{color:"{col}",scale:{sc},duration:.12,ease:"power1.out"}},{wt:.2f}).to("#{cid}_w{j}",{{scale:1,duration:.18,ease:"power1.in"}},{wt+.12:.2f});')
    t+=dur
TOTAL=round(t+OUTRO,2)

# HOOK card
hook=f'''<div id="hookcard" class="clip" data-start="0" data-duration="{INTRO:.2f}" data-track-index="7"
 style="position:absolute;inset:0;background:radial-gradient(circle at 50% 38%,#2A1846 0%,#08080d 78%);
 display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 70px">
 <div id="hooktop" style="font-family:Arial,sans-serif;font-weight:700;font-size:34px;color:#D4AF37;letter-spacing:2px;line-height:1.4;margin-bottom:30px">THEY CAME A THOUSAND MILES<br>FOR A BOY THEY NEVER MET</div>
 <div id="hookbig" style="font-family:'Arial Black',Arial;font-weight:900;font-size:104px;color:#fff;line-height:1.04">WHY?</div>
 <div id="hooksub" style="font-family:Arial,sans-serif;font-weight:700;font-size:30px;color:#bbb;letter-spacing:3px;margin-top:34px">ASK EVERY ONE OF THEM</div></div>'''
tl_js.insert(0,f'tl.fromTo("#hooktop",{{opacity:0,y:18}},{{opacity:1,y:0,duration:.6,ease:"power2.out"}},.3);')
tl_js.insert(1,f'tl.fromTo("#hookbig",{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:.7,ease:"back.out(1.5)"}},.9);')
tl_js.insert(2,f'tl.fromTo("#hooksub",{{opacity:0}},{{opacity:1,duration:.5}},1.7);')
tl_js.insert(3,f'tl.to("#hookcard",{{opacity:0,duration:.5,ease:"power1.in"}},{INTRO-.5:.2f});')

# OUTRO card
o=t
outro=f'''<div id="outrocard" class="clip" data-start="{o:.2f}" data-duration="{OUTRO:.2f}" data-track-index="7"
 style="position:absolute;inset:0;background:radial-gradient(circle at 50% 42%,#2A1846 0%,#08080d 80%);
 display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:0 60px">
 <div id="o1" style="font-family:'Arial Black',Arial;font-weight:900;font-size:64px;color:#E8C84A;line-height:1.1;margin-bottom:24px">SELF-DEFENSE<br>IS NOT MURDER</div>
 <div id="o2" style="font-family:'Arial Black',Arial;font-weight:900;font-size:50px;color:#fff;margin-bottom:36px">FREE KARMELO ANTHONY</div>
 <div id="o3" style="font-family:Arial,sans-serif;font-weight:700;font-size:44px;color:#D4AF37;letter-spacing:1px">freekarmelo.net</div></div>'''
tl_js.append(f'tl.fromTo("#o1",{{opacity:0,y:26}},{{opacity:1,y:0,duration:.6,ease:"power3.out"}},{o+.2:.2f});')
tl_js.append(f'tl.fromTo("#o2",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.5,ease:"power2.out"}},{o+.9:.2f});')
tl_js.append(f'tl.fromTo("#o3",{{opacity:0}},{{opacity:1,duration:.5}},{o+1.5:.2f});')

html=f'''<!doctype html>
<html lang="en"><head><meta charset="UTF-8"/><meta name="viewport" content="width={W}, height={H}"/>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>*{{margin:0;padding:0;box-sizing:border-box}}html,body{{width:{W}px;height:{H}px;overflow:hidden;background:#000}}</style>
</head><body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
{hook}
{chr(10).join(clip_html)}
{outro}
</div>
<script>
window.__timelines=window.__timelines||{{}};
const tl=gsap.timeline({{paused:true}});
{chr(10).join(tl_js)}
window.__timelines["main"]=tl;
</script></body></html>'''
open(f"{PROJ}/index.html","w").write(html)
print(f"✓ FULL MONTAGE: {TOTAL}s · {len(SEGS)} testimonies · {cap_idx} caption lines · hook {INTRO}s + outro {OUTRO}s")
