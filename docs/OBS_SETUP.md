# OBS setup for Biscuit Demo

Create one reusable OBS scene named **Biscuit Demo** and use it for every hackathon unless the project has unusual capture needs.

## Video

- Canvas: 1920×1080
- Output: 1920×1080
- FPS: 30
- Keep browser/editor/terminal text large enough to read in the final 1080p file.

## Audio

- Sample rate: 48 kHz
- Add the microphone you actually intend to narrate with.
- Add application/system audio only when the project needs it.
- Make a short recording and listen to the exported file. Moving meters are not proof that the final track is usable.

## Recording

Prefer **MKV** while recording. If OBS or the machine crashes, MKV is much less likely to lose the whole recording than MP4.

After recording, use OBS **File → Remux Recordings** to create an MP4 for upload when the hackathon requires MP4.

## Scene sources

Recommended source order, top to bottom:

1. Optional title-card group
2. Biscuit Logic tag
3. Project/window capture
4. Optional background
5. Audio sources

The project should occupy almost the whole frame.

## Biscuit Logic tag

Add a **Browser Source**:

- Name: `Biscuit Logic Tag`
- Check **Local file**
- Select `assets/biscuit-logic-tag.html` from this repository
- Width: 1920
- Height: 1080
- FPS: 30 is sufficient

The HTML positions the tag itself in the bottom-right corner. Keep the browser source full-frame so the CSS positioning remains predictable.

For `branding.mode = none`, hide the Browser Source.

For `branding.mode = subtle`, leave only the tag visible.

For `branding.mode = intro`, use the tag plus a short project title card at the beginning. Do not make an elaborate animated ident. The project is the star.

## Privacy pass

Before recording:

- enable Do Not Disturb / Focus
- close private chats and email
- hide API keys and tokens
- close unrelated browser tabs
- check terminal history before maximising a terminal
- avoid capturing the whole desktop when a single window capture will do

## 20-second acceptance test

Before the real demo, record twenty seconds containing:

1. the project window
2. your voice
3. project audio, if relevant
4. the Biscuit Logic tag

Watch the result back. If all four are correct, the capture rig is ready.
