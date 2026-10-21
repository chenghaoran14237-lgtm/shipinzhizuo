#!/usr/bin/env python3
"""Validate a scene-plan, including the opt-in 1.1 motion contract."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from schemas.artifacts import validate_artifact  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate OpenMontage scene_plan JSON and frame-exact MotionBeats."
    )
    parser.add_argument("scene_plan", type=Path)
    parser.add_argument("--report", type=Path, help="Optional JSON report path")
    args = parser.parse_args()

    try:
        data = json.loads(args.scene_plan.read_text(encoding="utf-8"))
        validate_artifact("scene_plan", data)
    except Exception as exc:
        report = {"valid": False, "path": str(args.scene_plan), "error": str(exc)}
        rendered = json.dumps(report, ensure_ascii=False, indent=2)
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(rendered, encoding="utf-8")
        print(rendered)
        return 1

    beat_count = sum(len(scene.get("motion_beats", [])) for scene in data["scenes"])
    cue_count = sum(len(scene.get("sound_cues", [])) for scene in data["scenes"])
    report = {
        "valid": True,
        "path": str(args.scene_plan),
        "version": data["version"],
        "scenes": len(data["scenes"]),
        "motion_beats": beat_count,
        "sound_cues": cue_count,
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
