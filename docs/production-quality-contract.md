# Editorial Animation Production Quality Contract

`scene_plan` 1.1 turns recurring production feedback into enforceable inputs
and gates. It is opt-in so completed 1.0 projects remain readable.

## What it prevents

| Production failure | Code-level constraint |
|---|---|
| A past internet wave is narrated as current | The plan records a reference date; the final review must report zero unsupported present-tense claims. |
| Real material becomes a small decorative minority | A minimum traceable-real-asset ratio of at least 35% is locked before asset production. |
| Archive material loses its texture under glossy effects | Diffuse light and low reflection are required; mirror glare, scanning light, full-frame glare and the generic black mystery stage are forbidden. |
| One approved still is treated as proof of the film | The sample must test at least four quality axes, followed by direction, asset, layout, animatic and candidate gates. |
| Every subject slowly drifts for the whole scene | Physical motion is split into frame-exact events with anticipation, short action, reaction, settle and visible result hold. |
| SFX suggests an action that is not visible | SFX may only reference a MotionBeat impact frame; it can instead be intentionally omitted. |
| Music is approved in isolation and disappears under voice | At least two relative levels are auditioned under real narration for 20 seconds or more. |
| A technically valid render is called complete | Compose requires a `production_quality_review` with all six gates passed, motion contact sheets and subtitle verification. |

## Commands

```bash
python scripts/validate_motion_plan.py \
  projects/<id>/artifacts/scene_plan.json \
  --report projects/<id>/artifacts/motion-plan-validation.json
python scripts/lint_remotion_motion.py \
  projects/<id>/FullComposition.tsx \
  --report projects/<id>/artifacts/remotion-motion-lint.json
python scripts/capture_motion_contact_sheet.py \
  projects/<id>/renders/candidate.mp4 \
  projects/<id>/artifacts/scene_plan.json \
  projects/<id>/snapshots/motion
```

The source lint allows a continuous exception only when the code includes a
nearby semantic annotation:

```ts
// motion-lint: allow-continuous -- the route line accumulates travel distance
```

Use the files in `examples/quality-contracts/` as copyable starting points.
The review example is evidence-shaped on purpose: changing a boolean to pass
without the cited files is a reviewer failure, not a substitute for inspection.
