# Chef Bot 3000

A content pipeline for an AI-generated cooking show. "Chef Bot 3000" is a comedic robot
chef character, and this project assembles the full media stack for episodes — scripts,
voiced audio, generated imagery, and 3D character assets.

## What's here

- **Episode scripts** — structured per-episode scripts (`episodes/<name>/script.json`).
- **Voice audio** — generated character voice lines and sound effects (`audio/`).
- **Imagery** — generated character/scene images, organized per episode (`image/`).
- **3D assets** — character models in glTF (`*.glb`) for animation/rendering.
- **Tooling** — helper scripts such as sequential image renaming (`image/imgs.py`).

## Concept

Take a recipe or food topic, generate a scripted episode in the Chef Bot persona, then
produce the matching voiceover, images, and 3D character assets so the episode can be
assembled end to end.

> Media-heavy creative project — the repo bundles generated assets alongside the tooling
> that produces and organizes them.
