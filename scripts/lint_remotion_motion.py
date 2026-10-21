#!/usr/bin/env python3
"""Reject Remotion primary motion stretched across scene-duration percentages.

This is intentionally a focused source lint, not a TypeScript parser. It finds
the failure mode that produced the all-scene slow drift in the Soulstealers
film: interpolation ranges derived from ``duration``/``durationInFrames`` and
fractional scene positions. Legitimate cumulative motion needs a nearby
``motion-lint: allow-continuous -- <semantic reason>`` comment.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ALLOW_RE = re.compile(r"motion-lint:\s*allow-continuous\s*--\s*\S+", re.IGNORECASE)
DURATION_TOKEN_RE = re.compile(r"\b(?:durationInFrames|sceneDuration|duration)\b")
FRACTIONAL_RANGE_RE = re.compile(
    r"(?:durationInFrames|sceneDuration|duration)\s*\*\s*(?:0?\.\d+|[a-zA-Z_$][\w$]*)"
)
WHOLE_RANGE_RE = re.compile(
    r"\[\s*(?:0\s*,\s*)?(?:durationInFrames|sceneDuration|duration)\s*\]"
)


def _line_number(source: str, offset: int) -> int:
    return source.count("\n", 0, offset) + 1


def lint_source(path: Path) -> list[dict[str, object]]:
    source = path.read_text(encoding="utf-8")
    lines = source.splitlines()
    findings: list[dict[str, object]] = []

    for match in re.finditer(r"\binterpolate\s*\(", source):
        window = source[match.start() : match.start() + 900]
        if not DURATION_TOKEN_RE.search(window):
            continue
        if not (FRACTIONAL_RANGE_RE.search(window) or WHOLE_RANGE_RE.search(window)):
            continue

        line = _line_number(source, match.start())
        nearby = "\n".join(lines[max(0, line - 5) : min(len(lines), line + 2)])
        if ALLOW_RE.search(nearby):
            continue

        excerpt = " ".join(window[:240].split())
        findings.append(
            {
                "path": str(path),
                "line": line,
                "rule": "no-full-scene-primary-interpolation",
                "message": (
                    "Interpolation derives its timing from scene duration. Use explicit "
                    "MotionBeat frame windows, or document genuinely cumulative motion with "
                    "`motion-lint: allow-continuous -- <semantic reason>`."
                ),
                "excerpt": excerpt,
            }
        )

    return findings


def _expand_paths(values: list[Path]) -> list[Path]:
    expanded: list[Path] = []
    for value in values:
        if value.is_dir():
            expanded.extend(sorted(value.rglob("*.tsx")))
            expanded.extend(sorted(value.rglob("*.ts")))
        else:
            expanded.append(value)
    return list(dict.fromkeys(expanded))


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint Remotion source for slow-drift timing patterns.")
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--report", type=Path, help="Optional JSON report path")
    args = parser.parse_args()

    findings: list[dict[str, object]] = []
    errors: list[str] = []
    paths = _expand_paths(args.paths)
    for path in paths:
        try:
            findings.extend(lint_source(path))
        except OSError as exc:
            errors.append(f"{path}: {exc}")

    report = {
        "valid": not findings and not errors,
        "files_checked": len(paths),
        "findings": findings,
        "errors": errors,
    }
    rendered = json.dumps(report, ensure_ascii=False, indent=2)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(rendered, encoding="utf-8")
    print(rendered)
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
