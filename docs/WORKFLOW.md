# Biscuit Demo workflow

This is the standard path for every hackathon project.

## 1. Add the demo packet early

From the Biscuit Logic repository:

```bash
python biscuit_demo.py init /path/to/project \
  --name "Project Name" \
  --tagline "One sentence saying what it does"
```

Do this while the project is still being built, not on submission night.

## 2. Make one known-good path

Choose the shortest sequence that proves the core idea works.

Save:

- stable input in `demo/sample-input/`
- representative output in `demo/sample-output/`
- useful fallback screenshots in `demo/screenshots/`

This should be honest evidence of the working system, not mocked functionality presented as live output.

## 3. Write the 90-second script

Edit `demo/demo-script.md`.

Prefer actions over explanations. If a sentence can be replaced by showing the result on screen, show the result.

## 4. Check the packet

```bash
python biscuit_demo.py check /path/to/project
```

Fix required packet errors. OBS and FFmpeg are machine-level capture tools, so they may be absent on build machines without invalidating the project packet.

## 5. Prepare the screen

- enable Focus / Do Not Disturb
- close private windows and unrelated tabs
- enlarge text
- hide secrets
- get the project into its starting state

## 6. Record a 20-second test

Use the reusable OBS scene and verify:

- readable picture
- clear narration
- project audio, if relevant
- Biscuit Logic tag, if allowed

Watch the test back.

## 7. Record the real demo

Aim for one clean take. Small spoken imperfections are fine. A comprehensible working product matters more than presenter polish.

## 8. Export and inspect

Remux/export to the submission format, then watch the exact final file from beginning to end before uploading it.

## Permanent rule

**A hackathon project is not finished until its useful behaviour can be demonstrated cleanly.**
