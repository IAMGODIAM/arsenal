# HYPERFRAMES MASTERY — Board Doctrine
*DAG: hyperframes-mastery-2026-0607 | Filed by Sue + Nova + Miranda | Board: IAMGODIAM*

**What it is:** HeyGen's open-source (Apache-2.0) HTML→MP4 engine. Write HTML+CSS+seekable
animation → renderer seeks each frame in headless Chrome → FFmpeg encodes. Deterministic:
same input = same output. Repo: github.com/heygen-com/hyperframes (25k★). Docs: hyperframes.mintlify.app.

## INSTALL AS AGENT SKILL (the real unlock)
```
npx skills add heygen-com/hyperframes   # registers slash skills
```
Requires Node 22+ and FFmpeg (we have FFmpeg). Slash skills it adds:
- `/hyperframes` — composition authoring (HTML, timing, captions, TTS, transitions)
- `/hyperframes-cli` — init, lint, inspect, preview, render, doctor
- `/hyperframes-media` — tts (Kokoro, no API key), transcribe, remove-background
- `/hyperframes-registry` — `hyperframes add <block>` (catalog blocks)
- `/gsap` — GSAP timeline/easing/plugins API

CLI loop (manual): `npx hyperframes init my-video` → `preview` (live browser) → `render` (MP4).

## THE 5 HARD RULES (break = broken render)
1. Register ALL timelines on `window.__timelines` — renderer can't seek what it doesn't know.
2. Video elements MUST be `muted` — audio goes in separate `<audio>` tracks for the mixer.
3. NO `Math.random()` — kills determinism. Use seeded PRNG (mulberry32) if needed.
4. Synchronous timeline construction — no async/await/fetch during GSAP setup.
5. Timed elements need `class="clip"` + `data-start` + `data-duration` + `data-track-index`.

Best-practice (auto-applied): entrance animation on EVERY scene; transition between EVERY scene.

## COMPOSITION SHAPE
```html
<div id="stage" data-composition-id="ID" data-start="0" data-width="1080" data-height="1920">
  <video class="clip" data-start="0" data-duration="6" data-track-index="0" src="clip.mp4" muted playsinline></video>
  <h1 class="clip" data-start="1" data-duration="4" data-track-index="1">Title</h1>
  <audio data-start="0" data-duration="6" data-track-index="2" data-volume="0.5" src="music.wav"></audio>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
  <script>
    const tl = gsap.timeline({ paused: true });
    tl.from("#title",{opacity:0,y:40,duration:0.8},1);
    window.__timelines = window.__timelines || {}; window.__timelines.ID = tl;
  </script>
</div>
```

## VOCABULARY → SETTINGS (say the word, get the result)
**Motion ease:** smooth=power2.out · snappy=power4.out · bouncy=back.out · springy=elastic.out · dramatic=expo.out · dreamy=sine.inOut
**Timing:** fast 0.2s=energy · medium 0.4s=pro · slow 0.6s=luxury · 1–2s=cinematic
**Caption tones:** Hype=heavy font + scale-pop 72–96px · Corporate=clean sans fade+slide 56–72 · Tutorial=mono typewriter · Storytelling=serif slow-fade 44–56 · Social=rounded bounce 56–80
**Per-word:** "karaoke word highlighting", "bigger brand names w/ accent", "bounce on emotional keywords", "highlight numbers differently"
**Transitions:** Calm=blur crossfade/cross-warp · Medium=push slide/whip pan · High=zoom through/glitch/ridged burn
**Marker highlights:** highlight=marker sweep · circle=hand-drawn ellipse · burst=radiating lines · scribble · sketchout=rect outline
**Audio-reactive:** bass→scale (pulse) · treble→glow · amplitude→opacity (breathing) · mids→shape. Keep text effects 3–6%, backgrounds 10–30%.
**TTS (Kokoro, local, no key):** af_heart/af_nova (warm female), am_adam (male), bf_emma/am_michael. Speed adjustable.
**Render quality:** draft (iterate) · standard (review) · high (final). Default 1920x1080 — SET 1080x1920 for vertical.

## CATALOG BLOCKS (install ready-made)
`npx hyperframes add flash-through-white` (shader transition) · `instagram-follow` (social overlay) · `data-chart` (animated chart). Browse: hyperframes.heygen.com/catalog.

## ANTI-PATTERNS
- No React/Vue — plain HTML + data-* + GSAP only.
- Don't ask 4K/60fps unless needed (default 1080p/30 is right for social).
- Warm-start beats cold-start: feed it a transcript/doc/URL and it grounds the copy.
- Iterate like talking to an editor ("make title 2x bigger", "add lower third at 0:03") — don't re-prompt from scratch.

## OUR DUAL-PATH STANDARD
- **ffmpeg-direct** (build_v3_synced.py) = sovereign baseline. Fast (47–84s/seg), zero deps, total control. Use for testimony/raw-footage films.
- **HyperFrames** = premium motion-graphics path. Kinetic captions, transitions, charts, branded hooks. Use for social hooks, launch videos, data viz.
- frame.md: invert e5enclave DESIGN tokens for the camera (Black-First Sovereign: midnight-purple, obsidian, gold filigree) so agent composes on-brand without guessing.

---
*DAG: hyperframes-mastery-2026-0607 · By Grace, perfect ways. 🐉🎬*
