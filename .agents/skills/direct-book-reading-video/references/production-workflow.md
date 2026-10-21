# Production Workflow

## 1. Initialize and Bind the Series Style

Use the `animated-explainer` pipeline unless the brief clearly requires another declared OpenMontage pipeline. Initialize a separate project for every book and bind `style_playbook="book-reading-editorial"`.

Example:

```bash
python3 -c "
from lib.checkpoint import init_project
init_project(
    'book-slug-book-reading-YYYYMMDD',
    title='《书名》精读',
    pipeline_type='animated-explainer',
    style_playbook='book-reading-editorial',
)
"
```

Do not create a placeholder project merely to test the skill. Initialize only when a real book and title are known.

Use canonical pipeline artifacts and checkpoints. Keep series-specific direction in `art-direction.md` or a clearly linked artifact; keep provider, runtime, music, and approval decisions in the append-only decision log.

## 2. Research the Argument

Identify:

- the audience's likely prior belief;
- the book's most useful claim;
- the counterintuitive proposition;
- the mechanism that makes the proposition true;
- one or more concrete examples;
- the costs, limits, or second-order effects;
- the practical lens returned to the viewer.

Do not confuse a catchy claim with an accurate claim. Verify factual statements and preserve source URLs.

## 3. Write for Performance

Draft the opening before the whole script. The first beat should normally name the book, deliver the thesis, and create a reason to continue. Avoid biography, table-of-contents recitation, and generic endorsement.

Maintain two text views:

- editorial script: natural prose and argument structure;
- provider text: punctuation and segmentation designed for performance.

Keep related thoughts together. Split only at true rhetorical boundaries. Mark emphasis, contrast, difficult names, numerical readings, and intentional pauses. The opening title pause is about one second by default.

## 4. Distill Scenes Before Searching

Break scenes at changes in evidence, relationship, time, place, scale, or intellectual pressure—not at every sentence.

For each scene, define this contract before sourcing:

| Field | Required question |
|---|---|
| Claim | What must the viewer understand now? |
| Evidence slot | What exact person, object, place, document, event, or condition proves it? |
| Representative test | Why is this source specific enough rather than generic coverage? |
| Rights constraint | What provenance or license is acceptable? |
| Processing | What crop, layer separation, mask, grading, or annotation is needed? |
| Semantic verb | What meaningful action happens? |
| Setup | What relationship exists before the action? |
| Reaction | What visibly responds? |
| Result | What new state remains? |
| Camera | Why must attention or scale change? |
| Bridge | What visible element carries into the next scene? |

Do not start broad browsing until these slots exist. Stop searching when a slot works at final scale, has adequate provenance, and supports the planned action.

## 5. Acquire and Process Evidence

Prefer official documents, archives, institutional publications, licensed photographs, maps, charts, and traceable reporting. Store originals separately from derived files.

Process each source for its exact action:

- crop for subject and negative space;
- lightly normalize saturation and contrast;
- separate foreground, background, document, or object layers;
- mask areas that must accept labels;
- preserve identifying and evidentiary details;
- prepare deterministic cuts, folds, holes, ties, stamps, routes, or occlusions.

Never use generative repair, extension, or stylization without an explicit approved plan and provenance note. Never treat a downloaded image as finished art direction.

## 6. Prove Style, Then Prove Motion

Use the minimum representative stills needed to test palette, typography, source treatment, composition variety, and occlusion. Static approval does not authorize full production.

Create a short motion proof containing setup, action, reaction, result, and a transition. Judge it at original speed. It must demonstrate:

- evidence participates in the action;
- the primary verb is legible without narration;
- motion density is sufficient but not restless;
- camera movement has a reason;
- the result holds long enough to understand;
- the cut hands off a visible relationship.

If the proof looks like a poster with an entrance animation, return to scene direction instead of adding decoration.

## 7. Direct and Build Narration

Use the approved local voice profile when available. Keep private reference audio and transcript outside public project paths; record only approved profile identifiers and hashes.

For a meaningful performance change, produce a short A/B sample using the same text, model, voice, and generation settings. Change punctuation or segmentation deliberately and identify the exact difference. Obtain the user's selection before full synthesis when the pipeline gate requires it.

Build continuous thought units rather than sentence files. Preserve natural tails. Measure boundary energy and inspect every boundary that coincides with a scene change. Use a small release or crossfade only when needed; do not blanket-trim all tails.

## 8. Compose Natively in 4:3

Author at `1440x1080`, `30fps`. Reflow every scene for 4:3. Do not crop, add side bars, or non-uniformly scale a prior aspect ratio.

Use a 12-column editorial grid and reserve a bottom subtitle safety rail of roughly `136px` when full subtitles are enabled. Center subtitles mathematically at `x=720`; do not assume the text box is centered because its left edge looks balanced.

Show the opening book cover in full with contain-like behavior. Hold the opening visual through the spoken-title pause. Keep text away from dark or high-detail evidence; use a cold-white opaque rail or a localized contrast treatment when overlap cannot be avoided.

## 9. Pace by Meaning

Use short action windows and stable result holds. A useful starting vocabulary at 30fps is:

- hit or stamp: about 6–10 frames;
- snap or bind: about 10–16 frames;
- reveal or route: about 18–28 frames;
- multi-step explanation: about 30–50 frames;
- result hold: at least 21 frames when the viewer must read or infer.

These are defaults, not a global metronome. Make quick actions quick and complex relationships measured. Avoid continuous drift and identical easing across scenes.

## 10. Add Music and Mix

Resolve the music decision during proposal. When approved, use a modern, restrained documentary bed with clear licensing. Keep the music audible during pauses and duck it under narration with smooth attack and release.

Listen at representative openings, dense explanations, scene transitions, quiet pauses, and the ending. Validate integrated loudness and true peak, but do not choose the final balance from meters alone.

## 11. Review Efficiently

Run objective checks for complete decode, duration, resolution, frame rate, aspect ratio, audio presence, unexpected black frames, unintended silence, subtitle coverage and center, opening cover completeness, and audio peak safety.

Watch or listen to the exact surfaces machines cannot judge: semantic clarity, representative evidence, visual taste, movement purpose, voice emotion, natural tails, and music presence.

Use one representative contact sheet or motion proof when it can answer the question. Do not emit internal JSON as the primary deliverable.

## 12. Revise the Smallest Layer

Classify feedback before editing:

| Feedback | Preferred surface |
|---|---|
| Wrong claim or structure | Script and scene plan |
| Generic or weak evidence | Asset slot and affected scene |
| Meaningless action | Scene direction and animation |
| Subtitle misalignment | Subtitle/layout layer only |
| One abrupt spoken boundary | Local release/crossfade only |
| Music too quiet | Music gain/mix only |
| Approved picture, audio-only issue | Copy video stream and replace audio |

State what stays frozen. Verify the unchanged stream or asset when practical. Preserve each complete deliverable with an explicit version name and record the unique change.
