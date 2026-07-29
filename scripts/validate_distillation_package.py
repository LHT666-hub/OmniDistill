from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from common import load_jsonl, read_csv, read_json, split_ids


BASE_FILES = [
    "SKILL.md",
    "agents/openai.yaml",
    "manifest.json",
    "sources/source-index.csv",
    "references/evidence-ledger.csv",
    "references/knowledge.md",
    "references/taste.md",
    "references/heuristics.md",
    "references/workflows.md",
    "references/anti-patterns.md",
    "references/boundaries.md",
    "references/limitations.md",
    "tests/test-cases.jsonl",
    "validation/report.json",
    "updates/history.jsonl",
]
TEST_TYPES = {"known", "forward", "contrast", "boundary", "adversarial"}
TIER_VALUE = {"v0": 0, "v1": 1, "v2": 2, "v3": 3}


def meaningful(path: Path) -> bool:
    text = path.read_text(encoding="utf-8-sig").strip()
    return bool(text and "No validated entries." not in text)


def validate(package: Path) -> tuple[list[str], list[str], str]:
    errors: list[str] = []
    warnings: list[str] = []
    for relative in BASE_FILES:
        if not (package / relative).is_file():
            errors.append(f"Missing required file: {relative}")
    if errors:
        return errors, warnings, "v0"

    skill_text = (package / "SKILL.md").read_text(encoding="utf-8-sig")
    frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", skill_text, re.S)
    if not frontmatter:
        errors.append("SKILL.md lacks valid YAML frontmatter")
    else:
        keys = re.findall(r"^([A-Za-z0-9_-]+):", frontmatter.group(1), re.M)
        if keys != ["name", "description"]:
            errors.append("SKILL.md frontmatter must contain only name and description")

    manifest = read_json(package / "manifest.json")
    declared = manifest.get("declared_tier", "v0")
    if declared not in TIER_VALUE:
        errors.append(f"Invalid declared tier: {declared}")
        declared = "v0"

    sources = read_csv(package / "sources" / "source-index.csv")
    ledger = read_csv(package / "references" / "evidence-ledger.csv")
    accepted_ids = {row.get("claim_id", "") for row in ledger if row.get("status") in {"accepted", "revised"}}
    achieved = "v0"
    if sources and ledger and accepted_ids:
        bad_links = []
        source_ids = {row.get("source_id", "") for row in sources}
        for row in ledger:
            for source_id in split_ids(row.get("source_ids", "")):
                if source_id not in source_ids:
                    bad_links.append(f"{row.get('claim_id')}: {source_id}")
        if bad_links:
            errors.append(f"Evidence ledger has unknown source links: {', '.join(bad_links)}")
        else:
            achieved = "v1"

    operational_files = [
        package / "references" / "heuristics.md",
        package / "references" / "workflows.md",
        package / "references" / "anti-patterns.md",
        package / "references" / "boundaries.md",
    ]
    if achieved == "v1" and all(meaningful(path) for path in operational_files):
        achieved = "v2"

    try:
        test_cases = load_jsonl(package / "tests" / "test-cases.jsonl")
    except ValueError as exc:
        errors.append(str(exc))
        test_cases = []
    report = read_json(package / "validation" / "report.json")
    case_types = {case.get("type") for case in test_cases}
    results = report.get("tests", [])
    passed_types = {
        result.get("type")
        for result in results
        if result.get("status") == "pass" and result.get("reviewed") is True
    }
    if achieved == "v2":
        if TEST_TYPES.issubset(case_types) and TEST_TYPES.issubset(passed_types) and report.get("reviewed") is True:
            achieved = "v3"
        elif declared == "v3":
            errors.append("v3 requires reviewed passing known, forward, contrast, boundary, and adversarial tests")

    if TIER_VALUE.get(declared, 0) > TIER_VALUE[achieved]:
        errors.append(f"Declared tier {declared} exceeds achieved tier {achieved}")
    if TIER_VALUE.get(declared, 0) < TIER_VALUE[achieved]:
        warnings.append(f"Package qualifies for {achieved} but declares {declared}")
    if manifest.get("identity_policy") not in {"capability_only", "persona_optional", "persona_explicit"}:
        errors.append("Invalid identity_policy")
    if manifest.get("route_reviewed") is not True:
        errors.append("Mode route must be explicitly reviewed before package validation")
    if manifest.get("rollback_supported") is not True or not isinstance(manifest.get("build_sequence"), int):
        errors.append("Manifest lacks rollback/build lineage metadata")
    if manifest.get("accepted_claim_count") != len(accepted_ids):
        errors.append("manifest accepted_claim_count does not match evidence ledger")
    return errors, warnings, achieved


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a generated OmniDistill Skill package.")
    parser.add_argument("package", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    errors, warnings, achieved = validate(args.package.resolve())
    result = {"achieved_tier": achieved, "errors": errors, "warnings": warnings}
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        for warning in warnings:
            print(f"WARNING: {warning}")
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Achieved tier: {achieved}")
    return 2 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
