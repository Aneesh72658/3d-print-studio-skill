---
name: "3d-print-studio"
description: "Turn any idea, sketch, photo or broken STL into a print-ready 3D model with no CAD skills; for real objects, verify against web references and user photos until 99% outline accuracy, optionally with a team of agents."
---

# 3D Print Studio

For people who own or use a 3D printer but can't use Blender/Fusion/CAD, or who have an idea they can't draw. Claude models; the user talks, picks options, measures, and sends photos.

Use for: "make me a...", "STL for...", "I have an idea for...", "model this sketch/photo", "miniature of my car/house/product", "fix/resize this STL", "keychain/sign/lithophane", "my print failed", "what settings".

## Ground rules
- Plain language, sizes in mm, a picture at every decision.
- **No silent guesses.** Every number comes from the user, a measurement/photo, an official spec, a measured reference image, or an approved default. No final model before the spec is confirmed.
- **Never claim an accuracy you did not measure.** Report the measured number, the method, and what limits it. A limit is a reason to get better input, not a reason to stop.
- **One approval for everything.** Ask for approval exactly once: at the end of Phase 2, in a single combined question that covers the spec AND the whole run (team agents, research, browser use, all build/verify iterations, saving files to the user's PC, opening the slicer). After "Build it", never ask permission again — decide, act, and report results. Mid-run, ask the user only for input nobody else can supply (reference photos, a measurement). The only things that still need a separate explicit yes: spending money/buying anything, and starting a physical print.
- Original designs only: no trademarked logos/badges or copyrighted characters. Real vehicles/buildings: model the shape, leave brand badges off.
- Remember the user's printer. Bed sizes: Bambu A1 256³, A1 mini 180³, P1S/X1C 256³, Prusa MK4 250x210x220, Ender 3 220x220x250.

## Setup (workspace, once per session)
```bash
which openscad || (apt-get update -qq && apt-get install -y -qq openscad)
which prusa-slicer || apt-get install -y -qq prusa-slicer
pip install --break-system-packages -q trimesh manifold3d numpy matplotlib pillow shapely rtree opencv-python-headless scikit-image
[ -d ~/.local/share/OpenSCAD/libraries/BOSL2 ] || git clone -q --depth=1 https://github.com/BelfrySCAD/BOSL2.git ~/.local/share/OpenSCAD/libraries/BOSL2
```
- **Geometric/functional parts**: OpenSCAD + BOSL2, Customizer-ready variables at the top.
- **Curved/organic real objects** (cars, bodies, product shells): Python + manifold3d. Build smooth bodies by **lofting cross-sections** along the length; details as booleans; revolve for wheels/flares. Never approximate a curved object with stacked boxes.

## Modes
| User says | Mode |
| --- | --- |
| Clear object + sizes | A. Make it |
| Vague idea | B. 2-3 concept renders → pick → A |
| Sketch/photo of object or space | C. From picture → A |
| Miniature/replica of a **real** object | R. Replica with accuracy loop |
| Big or high-accuracy project, or user asks for agents | T. Team mode (with R) |
| Common item (keychain, sign, box, hook, Gridfinity, lithophane) | D. Quick makers |
| Sends STL/3MF | E. Fix & remix |
| Settings / failed print / material | F. Print advisor |

## Phase 1 — Interview
Ask only what's unknown, with AskUserQuestion (tappable options with concrete sizes, max 4 per round): purpose & context (ask for a photo), critical dimensions + how measured, fit type, fixing method, load & environment, look/colours, printer & material. For named products look up official dimensions.

## Phase 2 — Confirm the spec (mandatory gate)
Overall size, critical dims with source, features, fixing/fit, material, orientation, supports, **every assumption**. Replicas also: scale, accuracy target and tolerance. Below the spec, state in one line what "Build it" authorises (agents, research, iterations, saving to PC) so this is the one and only approval. Only build on "Build it".

## Phase 3 — Build
FDM rules: walls >= 1.6 mm (load >= 2.4); holes +0.3 mm; M3 clearance 3.4, M4 4.5; fits 0.25/side snug, 0.4 sliding; print-in-place gaps >= 0.4; threads pitch >= 1.5; flat base, overhangs <= 45°, chamfer bottom edges; text >= 6 mm tall; detail >= 0.5 mm (0.4 nozzle) — say which details are dropped and why.
Multi-part prints: split so each part prints flat without supports; alignment holes in **both** parts for short 1.75 mm filament pins. Offset split planes ~0.007 mm off mesh vertices.

## Phase 4 — Mesh integrity (every build)
Watertight and a single body per printed part; report/fix loose pieces, never drop them silently. Avoid coincident/tangent surfaces: cut volumes start outside the surface (outset copy), sink add-ons 0.1 mm into their base, nudge features off loft stations. Grooves must not cut the interior.

## Phase 5 — Verify against the spec
Measure every spec line on the mesh (cross-sections, ray casts): spec | measured | OK/FAIL; overhang patches with width; fits bed; **multi-view render gate (mandatory, every build, before anything is delivered or sliced):** render the actual exported STL(s) as images from ALL directions — front, rear, left, right, top, bottom, plus front-3/4 and rear-3/4 — for the assembled model AND each print part in its print orientation; Read every image and check: shape matches the spec/reference, nothing floating or missing, no holes/slivers/inverted surfaces (dark patches), details on the correct side, parts sit flat on the bed. Any defect → fix, rebuild, re-render; only a clean full set passes. Also: real slicer estimate (prusa-slicer CLI, ±20%). Fit-critical parts: 5-10 min test coupon.

## Mode R — Replica accuracy loop (target 99%)
**Target:** 99% of outline points in every needed view within **0.25 mm** of the reference at model scale (state the real-world equivalent), and every key dimension within 0.1 mm. Also show IoU, but it understates accuracy at low resolution.
1. **Identify the exact variant** (model code, year, facelift, market). Discard wrong-variant references (name collisions are common).
2. **Gather references from the web**: official dimensions, factory/service-manual body dimensions, orthographic blueprints, true square-on photos; always the largest original image, captured at native resolution. Record source, variant, resolution.
3. **Ask the user for photos of the actual object until coverage is enough**, with a precise shot list. After each upload say what's covered and which shot is still missing; keep asking.
4. **Measure**: scale every reference by a dimension identical across variants (e.g. wheelbase); robust outline extraction (remove borders/ground lines, per-column + per-row envelope); orthographic model silhouette at the same scale; small-shift registration; compute % outline within 0.25 mm both ways, IoU, profile differences along length and height, key dimensions; save colour overlays.
5. **Fix by measurement** (convert profile differences into model parameters), rebuild, re-verify integrity + spec, re-measure. Repeat.
6. **Separate real errors from reference problems** (wrong variant parts, self-inconsistent blueprints, line thickness vs resolution, deliberate print-necessity features). Show scores with and without justified exclusions.
7. **Loop until the target is met.** Never present a replica as final while below target. **Stuck rule:** if two consecutive fix rounds don't raise the score, or a view can't be measured reliably (accessories, perspective, wrong variant, poor resolution), stop guessing and ask the user for reference images of their own object — name exactly which shots (e.g. "straight-on rear from ~10 m, camera at waist height, daylight") plus one tape measurement — then continue the loop with them. Keep asking for the specific missing shot until the target is reached. Each round: versioned model (v2, v3...), accuracy report image, measured numbers, and the next input needed. When a route dead-ends, find another (other sources, other languages, sister models sharing the body, parts catalogs, the user's own photos and tape measurements).

**Photo shot list:** exactly side-on (both sides), front-on, rear-on; stand far (~10 m for a car) and zoom in, camera at half the object's height, aimed at the middle; whole object in frame, level ground, nothing in front; close-ups of special parts/accessories; one or two tape-measured dimensions for calibration.

## Mode T — Team mode (multiple agents)
Use when the user asks for agents, or when a replica/large project has many independent parts or research threads. Requires the Agent tool.
1. **Break the project into parts** by structure and requirement (e.g. a car: dimensions research, factory-manual research, reference-image hunt, part details; then front fascia, rear, glasshouse/roof, body sides/doors, wheels & arches, mirrors & rails, underside, mesh integrity & printability, accuracy measurement). List all parts (can be 50-100 for big projects) and **group them into focused agents** — one agent per coherent area, sized so agents don't duplicate each other. Tell the user the grouping and why.
2. **Shared workspace**: write a CONTEXT.md (goal, target, variant warnings, known facts, file layout) and have every agent read it first and write results to its own file (research/<topic>.md, ref images + INDEX.md, part modules). Every finding records its source and confidence.
3. **Tool ownership**: only ONE agent drives the browser at a time; others use WebSearch/WebFetch. Only the integrator edits the main build script; part agents deliver parameter changes or separate module files plus their own measured before/after numbers.
4. **Waves**: wave 1 research (in parallel, background) → wave 2 part builders, each measuring and fixing its own zone against the references → wave 3 integration by the lead: merge, mesh integrity, spec check, full accuracy measurement. Below target → new wave aimed at the worst zones.
5. **Dead-end registry (never repeat a dead end)**: keep a shared `research/DEAD_ENDS.md` (what | route tried | why it failed | agent | date). Every agent reads it BEFORE trying any source and never retries a listed one; when a route fails (blocked site, paywall, too-small image, wrong variant, unusable method) it appends a line immediately and switches to a different route. When re-tasking or spawning agents, paste the current registry into their prompt and message running agents when it changes. The lead re-tasks agents on gaps and asks the user for the specific photos/measurements no agent can find; paid sources are listed, never bought without the user's explicit OK.
6. Keep the user posted after each wave: score per view, what improved, what's next.

## Mode D — Quick makers
Keychain/tag (ring hole >= 4 mm), sign/plaque, lithophane (0.6-3.0 mm heightfield, white PLA, vertical), cookie cutter (0.8-1.2 mm edge), boxes with slide/snap/hinge/thread lids, Gridfinity (42 mm grid, 7 mm units), hook, clip, stand, plant pot, knob, spacer, PCB enclosure, gear. Confirm sizes in one short round.

## Mode E — Fix & remix
Report size/watertight/overhangs/fits bed; repair, resize, mirror, orient, flat-cut base, split with pins, add holes/text/tabs. Only remix files the user owns or may modify.

## Mode F — Print advisor
Settings tuned to purpose and printer; honest material trade-offs; failed print from a photo → most likely cause first + 2-3 fixes.

## Deliver
1. Files to `/mnt/user-data/outputs/<part>/`: print STL(s), assembled-view STL, source, previews, accuracy report (replicas), HOW TO PRINT.txt.
2. If the user's computer is linked: save to `~/Downloads/3D Print Studio/<part>/<version>/`; never overwrite earlier versions.
3. SendUserFile the preview + report + print STL.
4. Name multi-part files by the real object's sides.
5. Reply: what it is, spec table, measured accuracy + what limits it, time/grams, supports, file location, the next input that would improve it most.

Optional: open in the user's slicer via computer use (load the computer-use skill first). Never start a print without explicit go-ahead.

## Honest limits
- 0.4 mm nozzle: features under ~0.5 mm don't print at small scale — say so.
- Printers vary ~0.1-0.3 mm; test coupons for fits.
- Accuracy can't be verified beyond the references' resolution — get better references rather than overstate.
