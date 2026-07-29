from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from common import slugify, utc_now, write_json


LEDGER_FIELDS = [
    "claim_id", "claim_text", "claim_type", "layer", "mode",
    "evidence_level", "source_ids", "source_count",
    "independent_source_count", "recurrence_count", "attribution",
    "attribution_confidence", "counterevidence_reviewed",
    "counterevidence_ids", "scope", "conditions", "failure_conditions",
    "confidence", "status", "allowed_use", "notes",
]

SOURCE_FIELDS = [
    "source_id", "path", "sha256", "media_type", "source_kind",
    "author", "published_at", "access_level", "rights", "consent",
    "independence_group", "allowed_use", "notes",
]


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize an OmniDistill workspace.")
    parser.add_argument("--target", required=True)
    parser.add_argument("--purpose", required=True)
    parser.add_argument("--tier", choices=("v0", "v1", "v2", "v3"), default="v2")
    parser.add_argument("--output-root", type=Path, default=Path("workspaces"))
    parser.add_argument("--slug")
    args = parser.parse_args()

    slug = slugify(args.slug or args.target)
    workspace = (args.output_root / slug).resolve()
    if workspace.exists() and any(workspace.iterdir()):
        print(f"Refusing to overwrite non-empty workspace: {workspace}", file=sys.stderr)
        return 2

    for relative in (
        "sources/raw", "evidence", "extraction", "output", "tests",
        "validation", "updates", "snapshots",
    ):
        (workspace / relative).mkdir(parents=True, exist_ok=True)

    write_json(
        workspace / "project.json",
        {
            "schema_version": 1,
            "project_id": slug,
            "target_name": args.target,
            "purpose": args.purpose,
            "requested_tier": args.tier,
            "declared_tier": args.tier,
            "identity_policy": "capability_only",
            "distribution": "internal",
            "created_at": utc_now(),
        },
    )
    write_json(
        workspace / "route.json",
        {
            "schema_version": 1,
            "primary_mode": "",
            "supporting_modes": [],
            "reasons": [],
            "reviewed": False,
        },
    )
    for file_path, fields in (
        (workspace / "sources" / "source-index.csv", SOURCE_FIELDS),
        (workspace / "evidence" / "evidence-ledger.csv", LEDGER_FIELDS),
    ):
        with file_path.open("w", encoding="utf-8-sig", newline="") as handle:
            csv.writer(handle).writerow(fields)

    write_json(
        workspace / "extraction" / "capability.json",
        {
            "schema_version": 1,
            "skill": {
                "name": slugify(f"{args.target}-skill"),
                "description": f"Evidence-grounded capability distilled from authorized material about {args.target}.",
            },
            "knowledge": [],
            "taste": [],
            "heuristics": [],
            "workflows": [],
            "anti_patterns": [],
            "boundaries": [],
            "limitations": [],
        },
    )
    (workspace / "tests" / "test-cases.jsonl").touch()
    write_json(
        workspace / "validation" / "report.json",
        {"schema_version": 1, "reviewed": False, "tests": [], "notes": []},
    )
    print(workspace)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
