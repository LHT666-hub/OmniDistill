from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path
from typing import Any

from common import read_csv, read_json, split_ids, utc_now, write_csv, write_json
from validate_evidence_ledger import validate as validate_ledger


LEDGER_OUTPUT_FIELDS = [
    "claim_id", "claim_text", "layer", "evidence_level", "source_ids",
    "attribution", "scope", "conditions", "failure_conditions", "confidence",
    "status", "allowed_use", "counterevidence_ids",
]


def markdown_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def item_claim_ids(item: dict[str, Any]) -> list[str]:
    value = item.get("claim_ids", [])
    if isinstance(value, str):
        return split_ids(value)
    return [str(part).strip() for part in value if str(part).strip()]


def collect_items(capability: dict[str, Any]) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for section in (
        "knowledge", "taste", "heuristics", "workflows",
        "anti_patterns", "boundaries", "limitations",
    ):
        values = capability.get(section, [])
        if not isinstance(values, list):
            raise ValueError(f"{section} must be a list")
        for item in values:
            if not isinstance(item, dict):
                raise ValueError(f"{section} entries must be objects")
            items.append(item)
    return items


def render_section(title: str, values: list[dict[str, Any]]) -> str:
    lines = [f"# {title}", ""]
    if not values:
        return "\n".join(lines + ["No validated entries.", ""])
    for item in values:
        item_id = item.get("id", "UNSET")
        heading = item.get("title") or item.get("statement") or item.get("name") or item_id
        lines.extend([f"## {item_id}: {heading}", ""])
        if item.get("statement") and item.get("statement") != heading:
            lines.extend([str(item["statement"]).strip(), ""])
        for label, key in (
            ("Trigger", "trigger"),
            ("Inputs", "inputs"),
            ("Conditions", "conditions"),
            ("Reason", "reason"),
            ("Outputs", "outputs"),
            ("Stop conditions", "stop_conditions"),
            ("Failure conditions", "failure_conditions"),
            ("Repair", "repair"),
            ("Scope", "scope"),
        ):
            if item.get(key):
                lines.append(f"- **{label}:** {item[key]}")
        steps = item.get("steps", [])
        if steps:
            lines.extend(["", "### Steps", ""])
            for number, step in enumerate(steps, 1):
                lines.append(f"{number}. {step}")
        claims = item_claim_ids(item)
        if claims:
            lines.extend(["", f"**Evidence claims:** {', '.join(claims)}"])
        lines.append("")
    return "\n".join(lines)


def render_skill(project: dict[str, Any], capability: dict[str, Any]) -> str:
    meta = capability["skill"]
    name = meta["name"]
    description = str(meta["description"]).replace("\n", " ").strip()
    purpose = project["purpose"]
    return f"""---
name: {name}
description: {description}
---

# {project["target_name"]}: distilled capability

Use this Skill for: {purpose}

## Operating sequence

1. Clarify the task, context, constraints, and desired artifact.
2. Read only the relevant files under `references/`.
3. Apply explicit quality criteria before selecting a heuristic or workflow.
4. State material assumptions and evidence limits.
5. Stop or ask when a boundary applies.
6. Never claim to be the source person or organization.

## Capability map

- Read `references/knowledge.md` for domain facts and concepts.
- Read `references/taste.md` for priorities and quality criteria.
- Read `references/heuristics.md` for conditional decision rules.
- Read `references/workflows.md` for executable procedures.
- Read `references/anti-patterns.md` before recommending action.
- Read `references/boundaries.md` and `references/limitations.md` before high-impact use.
- Use `references/evidence-ledger.csv` to audit provenance.

## Evidence discipline

Treat this Skill as an evidence-grounded model of capability, not a digital clone. Distinguish direct evidence, recurrent patterns, inference, and uncertainty. Do not extend a rule beyond its declared scope or failure conditions.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Assemble an executable Skill from curated OmniDistill artifacts.")
    parser.add_argument("workspace", type=Path)
    args = parser.parse_args()
    workspace = args.workspace.resolve()
    project = read_json(workspace / "project.json")
    capability = read_json(workspace / "extraction" / "capability.json")
    route = read_json(workspace / "route.json")
    ledger = read_csv(workspace / "evidence" / "evidence-ledger.csv")
    sources = read_csv(workspace / "sources" / "source-index.csv")
    ledger_errors, ledger_warnings = validate_ledger(workspace)
    for warning in ledger_warnings:
        print(f"WARNING: {warning}")
    if ledger_errors:
        for error in ledger_errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 2
    if route.get("reviewed") is not True or not route.get("primary_mode"):
        print("Mode route must be populated and explicitly reviewed before assembly.", file=sys.stderr)
        return 2

    meta = capability.get("skill", {})
    name = meta.get("name", "")
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        print("Skill name must use lowercase letters, digits, and hyphens.", file=sys.stderr)
        return 2
    if not meta.get("description"):
        print("Skill description is required.", file=sys.stderr)
        return 2

    accepted = {
        row["claim_id"]
        for row in ledger
        if row.get("status") in {"accepted", "revised"}
    }
    items = collect_items(capability)
    if not items:
        print("capability.json has no synthesized capability entries.", file=sys.stderr)
        return 2
    unsupported: list[str] = []
    for item in items:
        claims = item_claim_ids(item)
        if not claims:
            unsupported.append(f"{item.get('id', 'UNSET')}: no claim_ids")
        for claim_id in claims:
            if claim_id not in accepted:
                unsupported.append(f"{item.get('id', 'UNSET')}: unsupported claim {claim_id}")
    if unsupported:
        for issue in unsupported:
            print(f"ERROR: {issue}", file=sys.stderr)
        return 2

    package = workspace / "output" / name
    if package.exists():
        snapshot = workspace / "snapshots" / f"{name}-{utc_now().replace(':', '-')}"
        snapshot.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(package, snapshot)
        shutil.rmtree(package)
    (package / "references").mkdir(parents=True)
    (package / "sources").mkdir()
    (package / "tests").mkdir()
    (package / "validation").mkdir()
    (package / "updates").mkdir()
    (package / "agents").mkdir()

    (package / "SKILL.md").write_text(render_skill(project, capability), encoding="utf-8", newline="\n")
    (package / "agents" / "openai.yaml").write_text(
        "interface:\n"
        f"  display_name: \"{project['target_name']}\"\n"
        "  short_description: \"基于可追踪证据生成的专业能力 Skill\"\n"
        f"  default_prompt: \"Use ${name} to address this task with its validated heuristics, workflows, and boundaries.\"\n",
        encoding="utf-8",
        newline="\n",
    )
    section_names = {
        "knowledge": "Knowledge",
        "taste": "Taste",
        "heuristics": "Heuristics",
        "workflows": "Workflows",
        "anti_patterns": "Anti-patterns",
        "boundaries": "Boundaries",
        "limitations": "Limitations",
    }
    for key, title in section_names.items():
        (package / "references" / f"{key.replace('_', '-')}.md").write_text(
            render_section(title, capability.get(key, [])),
            encoding="utf-8",
            newline="\n",
        )
    write_csv(
        package / "references" / "evidence-ledger.csv",
        [row for row in ledger if row.get("status") in {"accepted", "revised"}],
        LEDGER_OUTPUT_FIELDS,
    )
    write_csv(
        package / "sources" / "source-index.csv",
        [
            {**row, "path": "" if row.get("allowed_use") == "internal_only" else row.get("path", "")}
            for row in sources
        ],
        list(sources[0].keys()) if sources else [
            "source_id", "path", "sha256", "media_type", "source_kind",
            "author", "published_at", "access_level", "rights", "consent",
            "independence_group", "allowed_use", "notes",
        ],
    )
    shutil.copy2(workspace / "tests" / "test-cases.jsonl", package / "tests" / "test-cases.jsonl")
    shutil.copy2(workspace / "validation" / "report.json", package / "validation" / "report.json")
    observation_path = workspace / "updates" / "observations.jsonl"
    history_path = package / "updates" / "history.jsonl"
    if observation_path.exists():
        shutil.copy2(observation_path, history_path)
    else:
        history_path.touch()
    snapshot_count = len([path for path in (workspace / "snapshots").glob(f"{name}-*") if path.is_dir()])
    write_json(
        package / "manifest.json",
        {
            "schema_version": 1,
            "name": name,
            "target": project["target_name"],
            "purpose": project["purpose"],
            "requested_tier": project["requested_tier"],
            "declared_tier": project.get("declared_tier", project["requested_tier"]),
            "identity_policy": project.get("identity_policy", "capability_only"),
            "distribution": project.get("distribution", "internal"),
            "modes": [route.get("primary_mode"), *route.get("supporting_modes", [])],
            "route_reviewed": route.get("reviewed") is True,
            "rollback_supported": True,
            "snapshot_count": snapshot_count,
            "build_sequence": snapshot_count + 1,
            "built_at": utc_now(),
            "accepted_claim_count": len(accepted),
        },
    )
    print(package)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
