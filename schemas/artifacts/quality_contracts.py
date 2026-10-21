"""Cross-field validation for opt-in production quality contracts.

JSON Schema is responsible for shape. These checks enforce relationships
between frames, causal beats, source policy, and sound anchors that cannot be
expressed clearly in the schema alone.
"""

from __future__ import annotations

from typing import Any


GENERIC_ONLY_VERBS = {
    "appear",
    "display",
    "fade",
    "fade in",
    "fade out",
    "pop",
    "show",
    "slide",
    "zoom",
    "出现",
    "展示",
    "显示",
    "淡入",
    "淡出",
    "滑入",
    "放大",
    "缩小",
}

CONTACT_KINDS = {"drop", "clamp", "strike", "stamp", "weigh", "tear", "compress"}
PHYSICAL_KINDS = CONTACT_KINDS | {"slide", "hinge", "bind", "displace", "withdraw"}


def _fail(path: str, message: str) -> None:
    raise ValueError(f"scene_plan 1.1 quality contract violation at {path}: {message}")


def _magnitude_is_legible(displacement: dict[str, Any] | None, threshold: float) -> bool:
    if not displacement:
        return False
    return any(
        (
            abs(float(displacement.get("x_short_axis_ratio", 0))) >= threshold,
            abs(float(displacement.get("y_short_axis_ratio", 0))) >= threshold,
            abs(float(displacement.get("rotation_degrees", 0))) >= 6,
            abs(float(displacement.get("scale_delta", 0))) >= threshold,
        )
    )


def validate_scene_plan_quality(data: dict[str, Any]) -> None:
    """Validate the semantic contract for a scene-plan 1.1 artifact.

    Version 1.0 intentionally bypasses these checks so existing projects and
    fixtures remain valid. New editorial-quality animation runs opt into 1.1.
    """

    if data.get("version") != "1.1":
        return

    contract = data["quality_contract"]
    motion_policy = contract["motion_policy"]
    fps = motion_policy["fps"]
    warning_max = motion_policy["warning_action_max_frames"]
    hard_max = motion_policy["hard_action_max_frames"]
    anticipation_min, anticipation_max = motion_policy["anticipation_range_frames"]
    reaction_min, reaction_max = motion_policy["reaction_range_frames"]
    min_hold = motion_policy["minimum_result_hold_frames"]
    min_displacement = motion_policy["minimum_primary_displacement_short_axis_ratio"]
    min_events, max_events = motion_policy["events_per_mechanism_scene"]

    scene_ids: set[str] = set()
    for scene_index, scene in enumerate(data["scenes"]):
        path = f"scenes[{scene_index}]"
        scene_id = scene["id"]
        if scene_id in scene_ids:
            _fail(f"{path}.id", f"duplicate scene id {scene_id!r}")
        scene_ids.add(scene_id)

        if scene["end_seconds"] <= scene["start_seconds"]:
            _fail(path, "end_seconds must be greater than start_seconds")

        semantic_verb = scene["semantic_verb"].strip().lower()
        if semantic_verb in GENERIC_ONLY_VERBS:
            _fail(
                f"{path}.semantic_verb",
                f"{scene['semantic_verb']!r} is animator-only; name the story action and consequence",
            )

        for asset_index, asset in enumerate(scene["required_assets"]):
            asset_path = f"{path}.required_assets[{asset_index}]"
            for field in ("id", "source_kind", "provenance_ref", "visual_role", "generative_processing"):
                if field not in asset:
                    _fail(asset_path, f"{field} is required by scene-plan 1.1")
            if asset["source_kind"] == "generated_ai" or asset["generative_processing"]:
                _fail(asset_path, "AI-generated visuals and generative processing are prohibited")

        motion_mode = scene["motion_mode"]
        beats = scene["motion_beats"]
        if motion_mode == "event" and not (min_events <= len(beats) <= max_events):
            _fail(
                f"{path}.motion_beats",
                f"event scenes require {min_events}-{max_events} discrete causal beats",
            )
        if motion_mode == "hold":
            if beats:
                _fail(f"{path}.motion_beats", "hold scenes must not hide decorative motion beats")
            if not scene.get("intentional_hold_reason"):
                _fail(f"{path}.intentional_hold_reason", "hold scenes need a narrative reason")
        if motion_mode == "continuous" and not beats:
            _fail(f"{path}.motion_beats", "continuous motion still needs a declared beat and visible result")

        scene_frames = round((scene["end_seconds"] - scene["start_seconds"]) * fps)
        beat_ids: set[str] = set()
        beat_by_id: dict[str, dict[str, Any]] = {}
        for beat_index, beat in enumerate(beats):
            beat_path = f"{path}.motion_beats[{beat_index}]"
            beat_id = beat["id"]
            if beat_id in beat_ids:
                _fail(f"{beat_path}.id", f"duplicate motion beat id {beat_id!r}")
            beat_ids.add(beat_id)
            beat_by_id[beat_id] = beat

            continuous = bool(beat.get("continuous"))
            anticipation = beat["anticipation_frames"]
            action = beat["action_frames"]
            reaction = beat["reaction_frames"]
            result_hold = beat["result_hold_frames"]

            if not continuous and not (anticipation_min <= anticipation <= anticipation_max):
                _fail(
                    f"{beat_path}.anticipation_frames",
                    f"event anticipation must be {anticipation_min}-{anticipation_max} frames",
                )
            if not continuous and not (reaction_min <= reaction <= reaction_max):
                _fail(
                    f"{beat_path}.reaction_frames",
                    f"event reaction must be {reaction_min}-{reaction_max} frames",
                )
            if not continuous and result_hold < min_hold:
                _fail(
                    f"{beat_path}.result_hold_frames",
                    f"visible result must hold for at least {min_hold} frames",
                )
            if action > hard_max and not continuous:
                _fail(
                    f"{beat_path}.action_frames",
                    f"primary action exceeds the hard limit of {hard_max} frames; split it into events",
                )
            if action > warning_max and not beat.get("timing_exception"):
                _fail(
                    f"{beat_path}.timing_exception",
                    f"actions longer than {warning_max} frames require a specific semantic exception",
                )

            total = (
                beat["start_frame"]
                + anticipation
                + action
                + reaction
                + beat["settle_frames"]
                + result_hold
            )
            if total > scene_frames:
                _fail(
                    beat_path,
                    f"beat ends at frame {total}, beyond the scene duration of {scene_frames} frames",
                )

            action_start = beat["start_frame"] + anticipation
            action_end = action_start + action
            if beat["kind"] in CONTACT_KINDS:
                impact = beat.get("impact_frame")
                if impact is None:
                    _fail(f"{beat_path}.impact_frame", "contact actions require a visible impact frame")
                if not action_start <= impact <= action_end:
                    _fail(
                        f"{beat_path}.impact_frame",
                        f"impact must fall inside the action window {action_start}-{action_end}",
                    )

            if beat["kind"] in PHYSICAL_KINDS and not _magnitude_is_legible(
                beat.get("displacement"), min_displacement
            ):
                _fail(
                    f"{beat_path}.displacement",
                    "physical actions need >=5% short-axis travel, >=6 degrees rotation, or an equivalent scale change",
                )

            if (
                motion_policy["forbid_full_scene_primary_interpolation"]
                and not continuous
                and action >= scene_frames * 0.7
            ):
                _fail(
                    f"{beat_path}.action_frames",
                    "a primary action may not be stretched across most of the scene",
                )

        cue_ids: set[str] = set()
        for cue_index, cue in enumerate(scene["sound_cues"]):
            cue_path = f"{path}.sound_cues[{cue_index}]"
            if cue["id"] in cue_ids:
                _fail(f"{cue_path}.id", f"duplicate sound cue id {cue['id']!r}")
            cue_ids.add(cue["id"])
            beat = beat_by_id.get(cue["motion_beat_id"])
            if beat is None:
                _fail(cue_path, f"unknown motion_beat_id {cue['motion_beat_id']!r}")
            if cue["role"] == "sfx":
                if cue["anchor"] != "impact":
                    _fail(f"{cue_path}.anchor", "SFX must be anchored to a visible impact")
                if "impact_frame" not in beat:
                    _fail(cue_path, "SFX cannot bind to a beat without impact_frame")


def validate_asset_manifest_quality(data: dict[str, Any]) -> None:
    """Require stable source pages for external assets in manifest v2."""

    if data.get("version") != "2.0":
        return

    external_kinds = {"archive", "artwork", "photograph", "footage", "audio_source"}
    seen: set[str] = set()
    for index, asset in enumerate(data["assets"]):
        path = f"asset_manifest 2.0 assets[{index}]"
        asset_id = asset["id"]
        if asset_id in seen:
            raise ValueError(f"{path}: duplicate asset id {asset_id!r}")
        seen.add(asset_id)
        provenance = asset["provenance"]
        if asset["source_kind"] in external_kinds and not provenance.get("original_url"):
            raise ValueError(f"{path}: external assets require an original source page URL")
        if provenance["derivative_path"] != asset["path"]:
            raise ValueError(
                f"{path}: provenance.derivative_path must match the executable asset path"
            )
