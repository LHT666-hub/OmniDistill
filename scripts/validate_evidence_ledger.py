from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import parse_int, read_csv, split_ids
from init_distillation_workspace import LEDGER_FIELDS


LAYERS = {"knowledge", "taste", "heuristic", "workflow", "anti-pattern", "boundary", "limitation"}
LEVELS = {"direct", "recurrent", "strong-inference", "weak-inference", "speculation", "counterevidence"}
ATTRIBUTIONS = {"individual", "team", "coauthor", "institution", "unknown", "not-applicable"}
STATUSES = {"proposed", "candidate", "tested", "accepted", "revised", "deprecated", "rejected"}


def validate(workspace: Path) -> tuple[list[str], list[str]]:
    ledger_path = workspace / "evidence" / "evidence-ledger.csv"
    source_path = workspace / "sources" / "source-index.csv"
    errors: list[str] = []
    warnings: list[str] = []
    if not ledger_path.exists() or not source_path.exists():
        return ["Missing evidence ledger or source index."], warnings
    ledger = read_csv(ledger_path)
    sources = read_csv(source_path)
    source_ids = {row.get("source_id", "") for row in sources}
    independence_groups = {
        row.get("source_id", ""): (row.get("independence_group", "").strip() or row.get("source_id", ""))
        for row in sources
    }
    if ledger:
        missing_fields = [field for field in LEDGER_FIELDS if field not in ledger[0]]
        if missing_fields:
            errors.append(f"Ledger is missing columns: {', '.join(missing_fields)}")
    claim_ids: set[str] = set()
    for row_no, row in enumerate(ledger, 2):
        claim_id = row.get("claim_id", "").strip()
        prefix = f"row {row_no} ({claim_id or 'missing claim_id'})"
        if not claim_id:
            errors.append(f"{prefix}: claim_id is required")
        elif claim_id in claim_ids:
            errors.append(f"{prefix}: duplicate claim_id")
        claim_ids.add(claim_id)
        if not row.get("claim_text", "").strip():
            errors.append(f"{prefix}: claim_text is required")
        if row.get("layer") not in LAYERS:
            errors.append(f"{prefix}: invalid layer {row.get('layer')!r}")
        if row.get("evidence_level") not in LEVELS:
            errors.append(f"{prefix}: invalid evidence_level")
        if row.get("attribution") not in ATTRIBUTIONS:
            errors.append(f"{prefix}: invalid attribution")
        if row.get("status") not in STATUSES:
            errors.append(f"{prefix}: invalid status")
        links = split_ids(row.get("source_ids", ""))
        missing = [value for value in links if value not in source_ids]
        if missing:
            errors.append(f"{prefix}: unknown source IDs {', '.join(missing)}")
        declared_count = parse_int(row.get("source_count", ""))
        if declared_count != len(set(links)):
            errors.append(f"{prefix}: source_count does not match unique source_ids")
        actual_independent = len({independence_groups.get(value, value) for value in links})
        declared_independent = parse_int(row.get("independent_source_count", ""))
        if declared_independent > actual_independent:
            errors.append(f"{prefix}: independent_source_count exceeds source independence groups")
        if row.get("status") in {"accepted", "revised"}:
            if row.get("evidence_level") in {"weak-inference", "speculation"}:
                errors.append(f"{prefix}: weak/speculative evidence cannot be accepted")
            if parse_int(row.get("independent_source_count", "")) < 2:
                errors.append(f"{prefix}: accepted rule requires at least 2 independent sources")
            if row.get("counterevidence_reviewed", "").lower() not in {"yes", "true"}:
                errors.append(f"{prefix}: accepted rule requires counterevidence review")
            if row.get("claim_type") == "personal-method" and row.get("attribution") == "unknown":
                errors.append(f"{prefix}: personal method cannot have unknown attribution")
        if row.get("claim_type") == "persona" and row.get("allowed_use") != "persona_optional":
            warnings.append(f"{prefix}: persona claims should be isolated as persona_optional")
        if row.get("confidence") == "high" and row.get("evidence_level") not in {"direct", "recurrent"}:
            errors.append(f"{prefix}: high confidence requires direct or recurrent evidence")
    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an OmniDistill evidence ledger.")
    parser.add_argument("workspace", type=Path)
    args = parser.parse_args()
    errors, warnings = validate(args.workspace.resolve())
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 2
    print("Evidence ledger is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
