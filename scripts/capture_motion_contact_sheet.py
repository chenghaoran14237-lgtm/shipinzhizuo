#!/usr/bin/env python3
"""Extract setup/action/reaction/result evidence from a rendered 1.1 plan."""

from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from schemas.artifacts import validate_artifact  # noqa: E402


def review_frames(scene: dict, fps: int) -> dict[str, int]:
    """Return absolute composition frames for the first causal beat."""

    beat = scene["motion_beats"][0]
    scene_start = round(scene["start_seconds"] * fps)
    action_start = beat["start_frame"] + beat["anticipation_frames"]
    action_end = action_start + beat["action_frames"]
    reaction_end = action_end + beat["reaction_frames"]
    settle_end = reaction_end + beat["settle_frames"]
    result_end = settle_end + beat["result_hold_frames"]

    return {
        "setup": scene_start + max(beat["start_frame"], action_start - 1),
        "action": scene_start + beat.get("impact_frame", action_start + beat["action_frames"] // 2),
        "reaction": scene_start + action_end + max(1, beat["reaction_frames"] // 2),
        "result": scene_start + settle_end + max(1, (result_end - settle_end) // 2),
    }


def _run(command: list[str]) -> None:
    subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create four-state motion evidence from a candidate render.")
    parser.add_argument("video", type=Path)
    parser.add_argument("scene_plan", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    if shutil.which("ffmpeg") is None:
        print("ffmpeg is required", file=sys.stderr)
        return 2

    plan = json.loads(args.scene_plan.read_text(encoding="utf-8"))
    validate_artifact("scene_plan", plan)
    if plan.get("version") != "1.1":
        print("contact-sheet extraction requires scene_plan version 1.1", file=sys.stderr)
        return 2

    fps = plan["quality_contract"]["motion_policy"]["fps"]
    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, object] = {
        "version": "1.0",
        "video": str(args.video),
        "scene_plan": str(args.scene_plan),
        "fps": fps,
        "scenes": [],
    }

    sequence = 0
    for scene in plan["scenes"]:
        if not scene["motion_beats"]:
            continue
        frame_map = review_frames(scene, fps)
        evidence: dict[str, object] = {"scene_id": scene["id"], "frames": {}}
        for state in ("setup", "action", "reaction", "result"):
            sequence += 1
            absolute_frame = frame_map[state]
            output = args.output_dir / f"frame-{sequence:04d}-{scene['id']}-{state}.png"
            _run(
                [
                    "ffmpeg",
                    "-y",
                    "-ss",
                    f"{absolute_frame / fps:.6f}",
                    "-i",
                    str(args.video),
                    "-frames:v",
                    "1",
                    str(output),
                ]
            )
            evidence["frames"][state] = {"frame": absolute_frame, "path": str(output)}
        manifest["scenes"].append(evidence)

    scene_count = len(manifest["scenes"])
    if scene_count:
        sheet = args.output_dir / "motion-contact-sheet.jpg"
        _run(
            [
                "ffmpeg",
                "-y",
                "-framerate",
                "1",
                "-pattern_type",
                "glob",
                "-i",
                str(args.output_dir / "frame-*.png"),
                "-vf",
                f"scale=420:-1,tile=4x{math.ceil(sequence / 4)}:padding=8:margin=8",
                "-frames:v",
                "1",
                str(sheet),
            ]
        )
        manifest["contact_sheet"] = str(sheet)

    manifest_path = args.output_dir / "motion-contact-sheet.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"ok": True, "manifest": str(manifest_path), "scenes": scene_count}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
