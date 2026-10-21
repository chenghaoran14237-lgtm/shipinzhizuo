---
name: "Cold-White Book-Reading Editorial Documentary"
version: "1.0"
tags:
  - "book close reading"
  - "editorial documentary"
  - "evidence-led animation"
  - "native 4:3"
author: "OpenMontage"
source_url: ""
created: "2026-08-13"

style_prompt_short: >
  A cold-white, contemporary editorial documentary in which traceable real photographs and documents remain the subject while precise local mechanism animation reveals cause, pressure, exchange, and consequence.

style_prompt_full: >
  Create a native 4:3 editorial documentary frame at 1440x1080. Use cold news white #F2F1ED as the main field, near-black #17191A for text and structure, steel blue-gray #52656E for secondary systems, causal red #C43D32 for one decisive relationship per scene, and warning amber #D89A2B only for risk. Use Source Han Sans SC for titles, body, and subtitles; Source Han Serif SC only for books or quoted documents; use a CJK monospaced face for dates, policy numbers, and sources. Treat traceable real photographs, official documents, maps, and archival material as large inspectable evidence, not thumbnails. Process them with restrained crop, layer separation, masking, and light saturation or contrast normalization while preserving identifying details. Attach graphics to evidence and stage one semantic action as setup, action, reaction, and visible result. Use brief stamps, binds, routes, splits, weights, reveals, and residual states; hold the result. Move the camera only when attention, scale, or causal relationship changes. Keep subtitles mathematically centered on an opaque cold-white safety rail when needed. Avoid warm vintage paper, sepia, corporate dashboards, generic icons, ordinary street filler, black text on dark photos, decorative lines, continuous drift, Ken Burns slideshows, poster sequences, and repeated fade-slide-zoom entrances.

colors:
  primary:
    - name: "News White"
      hex: "#F2F1ED"
      role: "main field, negative space, subtitle safety rail"
    - name: "News Near-Black"
      hex: "#17191A"
      role: "titles, body text, structural marks"
  accent:
    - name: "Causal Red"
      hex: "#C43D32"
      role: "one primary causal relation, policy action, or residual consequence"
    - name: "Warning Amber"
      hex: "#D89A2B"
      role: "rare risk, delay, or pressure marker"
  neutral:
    - name: "Steel Blue-Gray"
      hex: "#52656E"
      role: "secondary institutions, infrastructure, and explanatory depth"
    - name: "Source Gray"
      hex: "#747A7D"
      role: "source notes, dates, page numbers, inactive relations"

typography:
  display:
    family: "Source Han Sans SC"
    weight: "800-900"
    style: "sentence case, compact tracking, editorial hierarchy"
  body:
    family: "Source Han Sans SC"
    weight: "400-600"
    style: "high-contrast black on cold white, generous line height"
  caption:
    family: "Noto Sans Mono CJK SC"
    weight: "400-500"
    style: "small and precise for dates, policy numbers, sources, and provenance"
  rules:
    - "Use Source Han Serif SC only for book titles or genuine document quotations."
    - "Center full subtitles mathematically, not by eye."
    - "Never place black text directly over a dark or detailed photo."

layout:
  grid: "12-column editorial grid with 52px outer margins and 20px gutters"
  alignment: "asymmetrical editorial composition with one primary evidence subject"
  aspect_ratio: "4:3 native at 1440x1080"
  notes:
    - "Reserve roughly 136px at the bottom for a full subtitle safety rail."
    - "Let evidence occupy at least 55 percent of an evidence-led frame when practical."
    - "Alternate full evidence, split evidence, document inspection, close detail, and mechanism space."
    - "Show the opening book cover in full with contain-like behavior."

motion:
  transitions:
    - "visible evidence handoff"
    - "causal match cut"
    - "restrained hard cut"
    - "short documentary dissolve only when time or source changes"
  animation_style: >
    One authored semantic verb per scene, staged as setup, action, reaction, and result. Use short physical actions with readable consequence, then hold. Graphics emerge from or act upon the evidence; nothing drifts merely to remain animated.
  pacing: "Natural 1.0x: confirmations are quick, mechanisms measured, conclusions deliberate."
  audio_cues:
    - "Use sparse tactile contact sounds only on visible impacts or bindings."
    - "Use a restrained modern documentary music bed with smooth dialogue ducking when approved."

mood:
  keywords:
    - "lucid"
    - "credible"
    - "restrained"
    - "contemporary"
    - "analytical"
  era: "contemporary"
  cultural_reference: "Chinese current-affairs magazine design, public-document inspection, and authored editorial collage"
  avoid:
    - "warm yellow or sepia nostalgia"
    - "traditional PowerPoint composition"
    - "poster sequences with entrance animation"
    - "generic corporate blue dashboards"
    - "stock icon mosaics"
    - "decorative motion without meaning"

assets:
  reference_images: []
  gsep_elements: []
  html_snippets: []
  color_palette_image:
    url: ""

x_openmontage:
  playbook: "book-reading-editorial"
  pipeline: "animated-explainer"
  composition_mode: "atelier"
  width: 1440
  height: 1080
  fps: 30
---

## Design Principles

Real material is the grammatical subject; authored motion is the verb. The frame first establishes something the viewer can trust, then reveals the pressure, route, exchange, or consequence hidden inside it.

Reuse palette, typography, evidence discipline, motion logic, and review standards. Do not reuse a previous episode's finished scene, signature mechanism, or asset treatment unless the new argument independently demands it.

## OpenMontage Application

Bind new projects to `style_playbook="book-reading-editorial"`. Use the full series contract in the `direct-book-reading-video` skill for script, sourcing, voice, versioning, and QA rules that do not belong in a visual-style file.
