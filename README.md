# Biscuit Logic

> hello, Lucy 🍪

**Biscuit Demo** is a tiny reusable hackathon demo kit. Its job is simple: get a project from "it works on my machine" to a clear 60–90 second show-and-tell without turning the final evening into a video-production project.

## The default demo

1. **0–10 s:** What is it?
2. **10–20 s:** What problem does it solve?
3. **20–65 s:** Show the thing working: input → action → output.
4. **65–80 s:** Explain the interesting technical idea.
5. **80–90 s:** Finish with one memorable sentence.

The rule is: **show first, explain second.**

## Quick start

Requires Python 3.10+.

```bash
python biscuit_demo.py init /path/to/project \
  --name "Nexus Bunny Deluxe" \
  --tagline "An AI drummer that listens and performs with you"
```

That creates a `demo/` folder inside the target project containing:

```text
demo/
  demo-config.json
  demo-script.md
  demo-checklist.md
  sample-input/
  sample-output/
  screenshots/
```

Then run:

```bash
python biscuit_demo.py check /path/to/project
```

The check verifies the demo packet and reports whether OBS Studio and FFmpeg can be found on the machine.

## Branding

Biscuit Demo supports three branding modes:

- `subtle` — default. Small **BISCUIT LOGIC** signature bottom-right.
- `intro` — short Biscuit Logic title card plus the persistent signature.
- `none` — no branding for competitions that prohibit it.

The OBS overlay lives in `assets/biscuit-logic-tag.html`. Add it as a local Browser Source so the mark stays crisp at any capture resolution.

## Capture baseline

Our standard scene is intentionally boring and reliable:

- 1920×1080
- 30 fps
- 48 kHz audio
- project/window capture
- microphone
- application/system audio when the project needs it
- Biscuit Logic tag bottom-right
- record to MKV for crash safety
- remux to MP4 for submission

See [`docs/OBS_SETUP.md`](docs/OBS_SETUP.md).

## Philosophy

A hackathon build is not finished until it can be demonstrated cleanly. The demo should be treated as part of the product, not an emergency film made after the product.

Keep Biscuit Demo small. It is not a video editor, streaming framework, pitch-deck generator, or another project that needs its own project manager.
