---
name: direct-book-reading-video
description: Direct Chinese short-form book close-reading videos in OpenMontage with an evidence-led, cold-white editorial documentary style. Use for 书精读、读书短视频、书籍解读、知识纪录动画, or whenever the user asks to continue or reuse the established book-reading series style. Covers hook-first scripting, representative real-source planning, semantic mechanism animation, native 4:3 composition, local Mandarin voice direction, documentary music, minimal QA, and freeze-first revisions.
---

# Direct Book-Reading Video

Create a short-form explanation, not an animated book summary. Use representative real material as evidence, authored mechanism animation as explanation, and emotionally directed Mandarin narration as the story engine.

## Load the Series Contract

Read [references/series-contract.md](references/series-contract.md) before proposing an episode. It defines locked defaults, episode-level choices, and prohibited outcomes.

Before planning shots, sourcing media, generating narration, or composing, read [references/production-workflow.md](references/production-workflow.md). Follow the current OpenMontage pipeline and its human gates; this skill adds series-specific constraints and does not bypass `AGENT_GUIDE.md`.

Before presenting a motion proof, animatic, or final render, read [references/acceptance-checklist.md](references/acceptance-checklist.md). Run only checks that can change the delivery decision.

When a renderer or external design tool needs a portable prose style description, read [references/book-reading-editorial.visual-style.md](references/book-reading-editorial.visual-style.md). In OpenMontage, bind the project to the schema-validated playbook `book-reading-editorial`.

## Lock the Right Things

Use these series defaults unless the user explicitly revises them:

- Native `1440x1080`, `30fps`, `4:3`; never crop a finished 16:9 or stretch another ratio.
- Cold-white, contemporary editorial documentary treatment; real evidence is the subject and graphics explain it.
- Atelier authoring for a hero episode. Still present every available composition runtime and obtain approval as required by `AGENT_GUIDE.md`; never silently inherit Remotion merely because the reference episode used it.
- Natural `1.0x` Mandarin narration. Prefer the locally approved Qwen3-TTS 1.7B profile when available and authorized; keep private reference media local and identify it only by approved profile metadata.
- Complete, mathematically centered subtitles on an opaque cold-white safety rail when the image beneath is dark or busy.
- A visible full book cover at the opening, followed by about one second of intentional hold after the spoken title.
- An explicit music decision during proposal. When music is approved, use a restrained modern documentary bed with dialogue ducking; tune by listening rather than copying one fixed loudness number.

Treat the book, thesis, evidence, visual metaphor, semantic verbs, scene layouts, camera plan, accent use, music track, and final landing as episode-specific. Reuse the decision system, not finished creative components from a previous book.

## Direct the Episode

1. State one core thesis and one counterintuitive proposition before drafting the full script.
2. Open with the book and thesis. Do not begin with author biography, table of contents, or generic praise.
3. Break the narration by changes in ideas and relationships, not by sentence count.
4. Define what the viewer must see before searching. Give every source slot a claim, representative target, rights constraint, processing plan, semantic action, and visible result.
5. Give every scene one primary verb and stage it as `setup -> action -> reaction -> result`. Reject a scene whose complete action is only appear, fade, slide, zoom, or display.
6. Make photographs and documents participate in the mechanism: split, bind, route, stamp, weigh, fold, occlude, reveal, or transform according to the argument. Do not paste a downloaded rectangle into a card.
7. Move the camera only when attention, scale, or causal relationship changes. Let important evidence and conclusions hold long enough to read.
8. Prove visual taste with the minimum representative stills, then prove motion with a short setup/action/result sample. A good poster frame never proves an animation.
9. Synthesize narration in continuous thought units. Use real punctuation and segmentation for contrast, progression, and landing; do not claim unsupported natural-language emotion control. Inspect natural tails at scene boundaries before adding digital silence.
10. After approval, freeze stable layers. Patch a local audio boundary, subtitle position, or mix parameter without rerendering unaffected video whenever technically possible.

## Protect the Series from Template Drift

Reject generic streets, generic office towers, stock icon mosaics, corporate dashboards, warm vintage paper, all-vector scenes, continuous Ken Burns drift, poster sequences, and presentation-card animation.

Do not reuse the reference episode's roads, ledgers, gears, bridges, fiscal routes, scene layouts, or signature devices unless the new book independently requires the same real mechanism and the repetition is deliberately approved.

Every prominent line, label, camera move, and sound cue must carry information, redirect attention, or show consequence. Remove decorative motion instead of making it prettier.

## Hand Off Results

Lead with playable media rather than internal JSON. Summarize what changed, what remained frozen, and what the user should judge. Preserve provenance, decisions, timing, and QA evidence in the project workspace for audit and later revisions.
