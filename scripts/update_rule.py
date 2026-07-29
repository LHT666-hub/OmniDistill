from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import append_jsonl, load_jsonl, utc_now


def main() -> int:
    parser = argparse.ArgumentParser(description="Record and evaluate rule observations without silent drift.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add = subparsers.add_parser("add")
    add.add_argument("workspace", type=Path)
    add.add_argument("--rule-id", required=True)
    add.add_argument("--task-id", required=True)
    add.add_argument("--outcome", choices=("support", "contradict", "unclear"), required=True)
    add.add_argument("--evidence", default="")
    add.add_argument("--notes", default="")

    evaluate = subparsers.add_parser("evaluate")
    evaluate.add_argument("workspace", type=Path)
    evaluate.add_argument("--rule-id", required=True)
    args = parser.parse_args()

    path = args.workspace.resolve() / "updates" / "observations.jsonl"
    if args.command == "add":
        append_jsonl(
            path,
            {
                "schema_version": 1,
                "rule_id": args.rule_id,
                "task_id": args.task_id,
                "outcome": args.outcome,
                "evidence": args.evidence,
                "notes": args.notes,
                "recorded_at": utc_now(),
            },
        )
        print(path)
        return 0

    observations = [row for row in load_jsonl(path) if row.get("rule_id") == args.rule_id]
    support_tasks = {row.get("task_id") for row in observations if row.get("outcome") == "support"}
    contradictions = [row for row in observations if row.get("outcome") == "contradict"]
    if contradictions:
        print("review_required: contradictory observations exist")
        return 3
    if len(support_tasks) >= 3:
        print("eligible_for_tested: support reproduced across at least 3 tasks")
        return 0
    if len(support_tasks) >= 2:
        print("candidate: support reproduced across 2 tasks; collect another independent task")
        return 1
    print("observation_only: insufficient cross-task evidence")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
