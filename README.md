# 3D Print Studio — a Claude skill

**Turn any idea, sketch, photo or broken STL into a print-ready 3D model — no Blender, Fusion or CAD skills needed.**
You talk to Claude in plain words; Claude designs the part, checks it will print, and hands you the STL.

![Example: a 1:84 SUV keychain built and verified with this skill](examples/suv-keychain-renders.png)

## What it does

| You say | You get |
|---|---|
| "Make me a phone stand / bracket / box with a lid" | Asks only the questions that matter, confirms a spec, builds, verifies every dimension |
| "I have an idea but can't draw it" | 2–3 concept renders to pick from, then the real model |
| A sketch or a photo | Reads it, asks for the sizes a photo can't show, builds it |
| "A miniature of my car / house / product" | **Replica mode**: researches references, asks for your photos, and loops until **99% of the outline is within 0.25 mm** |
| A broken or wrong-size STL | Repair, resize, split for small beds, add holes/text |
| "My print failed" + photo | Most likely cause + fixes, best settings for your printer |

### Built-in quality gates
- **One approval** — a single "Build it" covers the whole job; no nagging mid-way.
- **Spec check** — every number measured on the finished mesh (spec vs measured table).
- **Mesh check** — watertight, single body per part, no hidden voids, no unprintable overhangs.
- **Picture check** — the STL is rendered from every direction and inspected before you see it.
- **Real slicer estimate** — print time and grams from PrusaSlicer.
- **Replica accuracy loop** — outline measured against references point by point; asks you for the exact photo it needs when stuck.
- **Team mode** — splits big jobs across multiple Claude agents with a shared **dead-end registry** so no source is tried twice.

## Install

**Claude (claude.ai / desktop app):** download `3d-print-studio.zip` from the [latest release](../../releases) → Settings → Capabilities → Skills → Upload skill.

**Claude Code:**
```bash
git clone https://github.com/Aneesh72658/3d-print-studio-skill.git
mkdir -p ~/.claude/skills && cp -r 3d-print-studio-skill/3d-print-studio ~/.claude/skills/
```

Then just ask: *"Make me a wall hook for 2 kg, screws 40 mm apart"* or *"Make a keychain of my car"*.

The skill installs its own tools in Claude's workspace (OpenSCAD + BOSL2, PrusaSlicer, trimesh, manifold3d). Standalone helpers are in [`tools/`](tools):
- `stl_check.py model.stl [bed_mm]` — size, watertight, volume, overhang area, bed contact + preview with overhangs in red
- `render_views.py model.stl out.png` / `render_six_views.py model.stl out.png` — multi-direction renders

## Honest limits
- Best at functional/geometric parts, enclosures, organisers, replicas of real objects. Weak at organic sculpts (faces, animals).
- 0.4 mm nozzles can't print details under ~0.5 mm; the skill tells you what it dropped.
- Replica accuracy can't beat your references — good square-on photos matter most.
- Original designs only: it won't copy logos, badges or copyrighted characters.

## Support / custom work
- ⭐ Star the repo if it helped you.
- 💖 [Sponsor](https://github.com/sponsors/Aneesh72658) to fund new modes and tools.
- 🛠 **Want it done for you** (custom models, replicas of your car or product, finished prints)? [Open a custom-model request](../../issues/new?template=custom-model-request.md).

## License
MIT — see [LICENSE](LICENSE).
