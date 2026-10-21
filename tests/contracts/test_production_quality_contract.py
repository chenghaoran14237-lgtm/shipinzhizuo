import json
from pathlib import Path

import pytest

from lib.checkpoint import CheckpointValidationError, _enforce_animation_quality_contract
from schemas.artifacts import validate_artifact
from scripts.capture_motion_contact_sheet import review_frames
from scripts.lint_remotion_motion import lint_source


ROOT = Path(__file__).resolve().parents[2]
PLAN_EXAMPLE = ROOT / "examples/quality-contracts/editorial-animation-scene-plan-v1.1.json"
REVIEW_EXAMPLE = ROOT / "examples/quality-contracts/editorial-animation-production-review.json"


def _plan() -> dict:
    return json.loads(PLAN_EXAMPLE.read_text(encoding="utf-8"))


def _review() -> dict:
    return json.loads(REVIEW_EXAMPLE.read_text(encoding="utf-8"))


def _materialize_review_evidence(tmp_path: Path, project_id: str, review: dict) -> None:
    project_dir = tmp_path / project_id
    evidence_paths: list[str] = []
    for gate in review["gates"].values():
        evidence = gate["evidence"]
        evidence_paths.extend([evidence] if isinstance(evidence, str) else evidence)
    evidence_paths.extend(
        [
            review["motion_review"]["contact_sheet_path"],
            review["reviewed_output_path"],
        ]
    )
    for scene in review["motion_review"]["scenes"]:
        evidence_paths.extend(
            [
                scene["setup_frame"],
                scene["action_frame"],
                scene["reaction_frame"],
                scene["result_frame"],
            ]
        )
    for relative in evidence_paths:
        path = project_dir / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"evidence")
    for field in ("plan_validation_report_path", "source_lint_report_path"):
        path = project_dir / review["motion_review"][field]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"valid": True}), encoding="utf-8")


def test_scene_plan_v11_example_is_valid() -> None:
    validate_artifact("scene_plan", _plan())


def test_scene_plan_v10_remains_backward_compatible() -> None:
    validate_artifact(
        "scene_plan",
        {
            "version": "1.0",
            "scenes": [
                {
                    "id": "legacy",
                    "type": "animation",
                    "description": "Legacy free-form motion",
                    "start_seconds": 0,
                    "end_seconds": 5,
                    "movement": "slow drift"
                }
            ]
        },
    )


def test_long_event_action_requires_a_specific_exception() -> None:
    plan = _plan()
    plan["scenes"][0]["motion_beats"][0]["action_frames"] = 60
    with pytest.raises(ValueError, match="timing_exception"):
        validate_artifact("scene_plan", plan)


def test_sfx_must_bind_to_a_visible_impact() -> None:
    plan = _plan()
    plan["scenes"][0]["sound_cues"][0]["anchor"] = "action_start"
    with pytest.raises(ValueError, match="SFX must be anchored"):
        validate_artifact("scene_plan", plan)


def test_production_review_requires_animatic_to_pass() -> None:
    review = _review()
    review["gates"]["animatic"]["status"] = "pending"
    with pytest.raises(Exception):
        validate_artifact("production_quality_review", review)


def test_compose_quality_gate_requires_binding_review(tmp_path: Path) -> None:
    with pytest.raises(CheckpointValidationError, match="production_quality_review"):
        _enforce_animation_quality_contract(
            tmp_path,
            "editorial-animation-example",
            "animation",
            "compose",
            "completed",
            {"scene_plan": _plan()},
        )


def test_compose_quality_gate_accepts_valid_review(tmp_path: Path) -> None:
    review = _review()
    _materialize_review_evidence(tmp_path, "editorial-animation-example", review)
    _enforce_animation_quality_contract(
        tmp_path,
        "editorial-animation-example",
        "animation",
        "compose",
        "completed",
        {"scene_plan": _plan(), "production_quality_review": review},
    )


def test_compose_quality_gate_rejects_missing_evidence(tmp_path: Path) -> None:
    with pytest.raises(CheckpointValidationError, match="missing evidence"):
        _enforce_animation_quality_contract(
            tmp_path,
            "editorial-animation-example",
            "animation",
            "compose",
            "completed",
            {"scene_plan": _plan(), "production_quality_review": _review()},
        )


def test_motion_source_lint_detects_scene_fraction_drift(tmp_path: Path) -> None:
    source = tmp_path / "Scene.tsx"
    source.write_text(
        "const p = interpolate(frame, [duration * 0.1, duration * 0.9], [0, 1]);\n",
        encoding="utf-8",
    )
    findings = lint_source(source)
    assert findings
    assert findings[0]["rule"] == "no-full-scene-primary-interpolation"


def test_motion_source_lint_allows_documented_continuous_motion(tmp_path: Path) -> None:
    source = tmp_path / "Scene.tsx"
    source.write_text(
        "// motion-lint: allow-continuous -- route accumulates travelled distance\n"
        "const p = interpolate(frame, [0, durationInFrames], [0, 1]);\n",
        encoding="utf-8",
    )
    assert lint_source(source) == []


def test_contact_sheet_frames_follow_causal_phases() -> None:
    plan = _plan()
    scene = plan["scenes"][0]
    frames = review_frames(scene, 30)
    assert frames["setup"] < frames["action"] < frames["reaction"] < frames["result"]


def test_asset_manifest_v1_remains_valid() -> None:
    validate_artifact(
        "asset_manifest",
        {
            "version": "1.0",
            "assets": [
                {
                    "id": "legacy-image",
                    "type": "image",
                    "path": "assets/images/a.png",
                    "source_tool": "provided",
                    "scene_id": "s1"
                }
            ]
        },
    )


def test_asset_manifest_v2_requires_source_page_for_external_material() -> None:
    manifest = {
        "version": "2.0",
        "policy": {"ai_generated_visuals": False, "generative_edits": False},
        "assets": [
            {
                "id": "archive-page",
                "type": "image",
                "path": "assets/images/page.png",
                "source_tool": "download",
                "scene_id": "s1",
                "source_kind": "archive",
                "director_role": "Primary source evidence",
                "provenance": {
                    "creator": "Archive",
                    "title": "Page",
                    "rights": "Public domain",
                    "access_date": "2026-08-06",
                    "source_path": "assets/source/page.tif",
                    "derivative_path": "assets/images/page.png",
                    "processing": ["crop"],
                    "sha256": "a" * 64,
                    "generative_processing": False
                }
            }
        ]
    }
    with pytest.raises(ValueError, match="source page URL"):
        validate_artifact("asset_manifest", manifest)
