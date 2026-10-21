# Edit Director - Animation Pipeline

## When To Use

This stage turns the scene plan into an animatic-grade edit plan. Timing is the product.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/edit_decisions.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["assets"]["asset_manifest"]`, `state.artifacts["scene_plan"]["scene_plan"]`, `state.artifacts["script"]["script"]` | Assets, timing plan, and beats |
| Playbook | Active style playbook | Motion and typography rules |

## Process

### 1. Protect Hold Time

After key reveals, plan enough time for the viewer to process the frame. Do not stack every scene edge to edge with motion.

### 2. Stagger Secondary Elements

Primary element first, supporting elements second. The edit decisions should reinforce hierarchy.

### 3. Keep Motion Meaningful

Motion should signal:

- emphasis,
- transition,
- transformation,
- contrast.

### 3b. Carry MotionBeats Into The Executable Timeline

For scene-plan 1.1, copy frame numbers from each `motion_beat`; do not rebuild
timing from scene percentages. The primary subject may not use an interpolation
whose input range spans most of `durationInFrames` unless the beat is declared
`continuous` with a semantic reason. Each event must retain distinct
anticipation, action, reaction, settle and result-hold phases.

Run the motion-plan validator and Remotion source lint before an animatic.
Render a low-resolution animatic with final narration timing, then watch it
completely at original speed. Log intervals where narration advances without
a new relationship, evidence, action or consequence. Do not start the
candidate merely because scene stills look good.

SFX is either bound to a declared MotionBeat `impact_frame` (offset no more
than ±6 frames) or explicitly omitted because the action is not visually
soundable. Never place SFX at an arbitrary timestamp to imply an action the
viewer cannot identify.

Audition music under real narration, over at least 20 seconds of representative
context, at two or more relative levels. Record the offsets and selected level;
isolated music playback does not prove a usable mix.

### 4. Use Metadata For Timing Detail

Recommended metadata keys:

- `hold_windows`
- `stagger_rules`
- `transition_map`
- `scene_timing_notes`

### 5. Quality Gate

- key information has enough dwell time,
- movement clarifies hierarchy,
- transitions stay consistent,
- the edit remains readable on the target platform.
- motion-plan validation and source lint pass,
- the final-voice animatic passes a complete original-speed review,
- SFX bindings reference visible impacts or have an explicit omission decision,
- music has been compared at two or more levels under narration.

## Common Pitfalls

- Overcrowding the timeline with continuous motion.
- Revealing all elements at once.
- Letting stylistic motion reduce readability.
