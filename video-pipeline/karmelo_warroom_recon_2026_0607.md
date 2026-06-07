# WAR ROOM RECON — FreeKarmelo 3-Min Master vs. HeyGen-Tier Craft
**DAG:** karmelo-warroom-recon-2026-0607 · Convened all-hands 2026-06-07
**Voices:** Wyrmcore (point) · Nova (motion) · Miranda (narrative) · LOGOS (voice) · LEX (legal gate) · MiroFish (scoring) · Atlas (docs)

---

## WYRMCORE OPENS
The Chairman asked the right question weeks ago: how does our cut stack against HeyGen-tier work?
The recon answer is sharper than expected: **HyperFrames IS HeyGen's own open-source engine**
(heygen-com/hyperframes). We are not chasing their tech — we are standing on it. Every gap from
here is **craft**, not capability. That is the best possible news: nothing blocks us but discipline.

Below: the master graded against the 6 craft techniques that separate scroll-stopping testimony
reels from competent ones. Each gets a verdict and a concrete generator upgrade.

---

## THE MASTER AS BUILT (anatomy)
- 2:57 · 1080×1920 · 30fps · audio −25.8 dB mean / −1.5 dB peak (full voices, not silent)
- 6 beats: HOOK(8s) → ANSWER → SON → DEF → STK → INS → OUTRO(16s)
- 15 testimony windows, 111 karaoke caption lines
- Captions at y=1360px (clears TikTok bottom UI ~1500px — but margin is thin)
- **Transitions: NONE. Pure hard cuts on fixed time windows.**

---

## GRADED AGAINST CRAFT (MiroFish scoring 0–100)

### 1. J/L CUTS — audio leads/trails the visual · SCORE: 35 ⬅ biggest gap
**Source rule (LucidLink/Fincher):** in dialogue, let the next voice START before its clip appears
(J-cut), or let the prior voice TRAIL into the next shot (L-cut). Hard ping-pong cutting "feels like
relentless back-and-forth." That is exactly our current feel — 15 windows, each audio locked to its
own clip boundary.
**Our state:** every `<audio data-start>` == its `<video data-start>`. Zero overlap. Mechanical.
**Upgrade:** offset incoming audio −0.4s before its video on emotional beats (SON, DEF). Generator:
add `AUDIO_LEAD=0.4` and start the audio clip earlier than the video on flagged windows.

### 2. TRAILING-WORD TRIM — cut on speech gaps, not time boundaries · SCORE: 40
**Source rule:** never cut mid-breath or mid-word; trim to the natural silence between phrases.
**Our state:** windows are hand-set (ss,ee) — some land mid-word because they're time-picked, not
gap-picked. We already run faster-whisper; we have word timestamps but don't use them for trim points.
**Upgrade:** snap each window's `ee` to the nearest whisper word-gap ≥150ms. qa_score.py can flag any
window whose end falls <80ms from a word's end (= clipped word).

### 3. CAPTION SAFE-ZONE · SCORE: 78 (passing, thin margin)
**Source rule (TikTok 2026):** keep text out of bottom ~320px (UI) and top ~130px.
**Our state:** captions at y=1360, bottom edge ~1450px. Clears the 1500px UI line by ~50px — works,
but a 2-line caption can spill. **Upgrade:** raise caption baseline to y=1280 (bottom ~1370px) for a
safe 130px buffer. One-line change: `top:{H-640}`.

### 4. HARD-CUT vs CROSSFADE · SCORE: 60
**Source rule:** hard cuts keep momentum (correct default for urgency); but a 6-frame crossfade on
BEAT transitions (between the 5 beat-headers) signals "new chapter" without breaking pace.
**Our state:** zero GSAP transitions — every beat slams. Reads slightly raw at beat changes.
**Upgrade:** add `tl.fromTo(beatHdr,{opacity:0},{opacity:1,duration:0.25},seg)` on the 5 beat cards
only. Testimony clips STAY hard-cut (momentum). Surgical, not blanket.

### 5. HOOK / FIRST 3 SECONDS · SCORE: 82 (strong)
**Source rule:** the first 3s decide retention. Our hook — "THEY CAME A THOUSAND MILES FOR A BOY THEY
NEVER MET / WHY?" — is genuinely strong: question-driven, high-contrast, curiosity gap. Keep it.
**Micro-upgrade:** drop a faint courtroom-ambience bed under the 8s hook card so it isn't dead-silent
before the first voice. Raises perceived production value.

### 6. MOTION / EYE-CANDY POLISH · SCORE: 55
**Source rule:** subtle continuous motion (slow push-in / parallax) keeps the eye even on static frames.
**Our state:** cards are static. Testimony video moves, but the 8s hook + 16s outro are still.
**Upgrade:** GSAP slow scale 1.0→1.06 over the hook and outro card lifetimes (Ken Burns). One tween each.

---

## MIROFISH COMPOSITE: 58/100
"Structurally sound, legally clean, emotionally sequenced — but edited like a slideshow, not a film.
The single highest-leverage fix is J/L cuts (technique 1): it's the difference between 15 separate
clips and one continuous testimony. Trailing-word trim (technique 2) is second. Both are powered by
whisper data we ALREADY generate. No new tooling, no cost — pure craft."

## LEX HOLDS THE GATE
All upgrades are presentation-layer. None touch the legal framing: courtroom clips stay attributed to
supporters, disclaimer card stays, presumption of innocence throughout, "murder" stays scrubbed from
on-screen text. **Cleared to proceed.**

---

## UPGRADE QUEUE (priority order)
1. **J/L cuts** — AUDIO_LEAD=0.4 on SON/DEF beats (generator) ⬅ do first
2. **Trailing-word trim** — snap window ends to whisper gaps ≥150ms
3. **qa_score.py auto-gate** — clipped-word flag + caption-Y + black-gap + audio-mean BEFORE delivery
4. **Caption safe-zone** — raise to y=1280
5. **Beat crossfades** — 0.25s opacity on 5 beat cards only
6. **Ken Burns** — slow scale on hook + outro cards
7. **Hook ambience bed** — faint courtroom room-tone under 8s hook

Then re-render, re-grade, target MiroFish ≥ 80, deliver 3-min + derive 60s/15s social cuts.

---
*Wyrmcore closes: nothing here is hard. It's a half-day of craft on tech we already own, powered by
data we already generate, at zero new cost. Sovereign-Build all the way down.*
*DAG: karmelo-warroom-recon-2026-0607 · By Grace, perfect ways. 🐉🎬*
