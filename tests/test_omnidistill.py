from __future__ import annotations

import csv
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run_script(name: str, *args: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / name), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    if result.returncode != expect:
        raise AssertionError(
            f"{name} returned {result.returncode}, expected {expect}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


class OmniDistillTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self) -> None:
        self.temp.cleanup()

    def init_workspace(self, tier: str = "v2") -> Path:
        run_script(
            "init_distillation_workspace.py",
            "--target", "Test Researcher",
            "--purpose", "Evaluate research ideas and design evidence",
            "--tier", tier,
            "--output-root", str(self.root),
        )
        return self.root / "test-researcher"

    def prepare_sources(self, workspace: Path) -> None:
        raw = workspace / "sources" / "raw"
        (raw / "paper-a.txt").write_text("A full paper with a documented decision.", encoding="utf-8")
        (raw / "interview-b.txt").write_text("An independent interview about the same decision.", encoding="utf-8")
        metadata = self.root / "metadata.csv"
        with metadata.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=[
                    "path", "source_kind", "author", "published_at", "access_level",
                    "rights", "consent", "independence_group", "allowed_use", "notes",
                ],
            )
            writer.writeheader()
            writer.writerow({
                "path": "paper-a.txt", "source_kind": "document", "author": "A",
                "published_at": "2025", "access_level": "full", "rights": "user-owned",
                "consent": "yes", "independence_group": "paper-a",
                "allowed_use": "as_declared", "notes": "",
            })
            writer.writerow({
                "path": "interview-b.txt", "source_kind": "interview", "author": "B",
                "published_at": "2026", "access_level": "full", "rights": "user-owned",
                "consent": "yes", "independence_group": "interview-b",
                "allowed_use": "as_declared", "notes": "",
            })
        run_script("register_sources.py", str(workspace), "--metadata", str(metadata))

    def prepare_ledger(self, workspace: Path, weak: bool = False) -> None:
        path = workspace / "evidence" / "evidence-ledger.csv"
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            fields = next(csv.reader(handle))
        rows = []
        layers = [
            ("C-001", "heuristic"),
            ("C-002", "workflow"),
            ("C-003", "anti-pattern"),
            ("C-004", "boundary"),
        ]
        for claim_id, layer in layers:
            rows.append({
                "claim_id": claim_id,
                "claim_text": f"Validated {layer} claim",
                "claim_type": "personal-method",
                "layer": layer,
                "mode": "research-mentor",
                "evidence_level": "weak-inference" if weak else "recurrent",
                "source_ids": "S-0001;S-0002",
                "source_count": "2",
                "independent_source_count": "2",
                "recurrence_count": "2",
                "attribution": "individual",
                "attribution_confidence": "medium",
                "counterevidence_reviewed": "yes",
                "counterevidence_ids": "",
                "scope": "research design",
                "conditions": "when evidence is available",
                "failure_conditions": "outside the documented domain",
                "confidence": "medium",
                "status": "accepted",
                "allowed_use": "core",
                "notes": "",
            })
        with path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)

    def prepare_capability(self, workspace: Path) -> None:
        capability = {
            "schema_version": 1,
            "skill": {
                "name": "test-researcher-skill",
                "description": "Evaluate research ideas using evidence-grounded criteria, workflows, anti-patterns, and boundaries.",
            },
            "knowledge": [{"id": "K-001", "statement": "Evidence must match the claim.", "claim_ids": ["C-001"]}],
            "taste": [{"id": "T-001", "statement": "Prefer explicit evidence tests.", "claim_ids": ["C-001"]}],
            "heuristics": [{
                "id": "H-001", "statement": "When evidence is incomplete, test the problem framing first.",
                "conditions": "Uncertain framing", "failure_conditions": "Purely operational task",
                "claim_ids": ["C-001"],
            }],
            "workflows": [{
                "id": "W-001", "title": "Evidence review", "trigger": "A new research idea",
                "inputs": "Idea and available evidence", "steps": ["Frame claim", "Check sources", "Test alternatives"],
                "outputs": "Review", "stop_conditions": "No auditable evidence", "claim_ids": ["C-002"],
            }],
            "anti_patterns": [{
                "id": "A-001", "statement": "Do not treat frequency as causality.",
                "repair": "Add negative cases and causal qualification", "claim_ids": ["C-003"],
            }],
            "boundaries": [{
                "id": "B-001", "statement": "Do not infer private beliefs from public papers.",
                "claim_ids": ["C-004"],
            }],
            "limitations": [{
                "id": "L-001", "statement": "Public artifacts omit failed unpublished work.",
                "claim_ids": ["C-004"],
            }],
        }
        (workspace / "extraction" / "capability.json").write_text(
            json.dumps(capability, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def test_mode_router_recommends_hybrid(self) -> None:
        output = self.root / "route.json"
        run_script(
            "route_modes.py",
            "--brief", "Distill a professor's papers, interviews, course material, and lab workflow into a research mentor",
            "--output", str(output),
        )
        route = json.loads(output.read_text(encoding="utf-8"))
        modes = {route["primary_mode"], *route["supporting_modes"]}
        self.assertIn("research-mentor", modes)
        self.assertIn("person-thinking", modes)
        self.assertIn("work-expert", modes)

    def test_initializer_refuses_overwrite(self) -> None:
        self.init_workspace()
        run_script(
            "init_distillation_workspace.py",
            "--target", "Test Researcher",
            "--purpose", "Different purpose",
            "--output-root", str(self.root),
            expect=2,
        )

    def test_register_sources_and_hashes(self) -> None:
        workspace = self.init_workspace()
        self.prepare_sources(workspace)
        with (workspace / "sources" / "source-index.csv").open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 2)
        self.assertEqual({row["independence_group"] for row in rows}, {"paper-a", "interview-b"})
        self.assertTrue(all(len(row["sha256"]) == 64 for row in rows))

    def test_ledger_rejects_weak_accepted_rule(self) -> None:
        workspace = self.init_workspace()
        self.prepare_sources(workspace)
        self.prepare_ledger(workspace, weak=True)
        run_script("validate_evidence_ledger.py", str(workspace), expect=2)

    def test_assembler_rejects_unreviewed_route(self) -> None:
        workspace = self.init_workspace()
        self.prepare_sources(workspace)
        self.prepare_ledger(workspace)
        self.prepare_capability(workspace)
        run_script("assemble_skill.py", str(workspace), expect=2)

    def test_end_to_end_v2_and_zip(self) -> None:
        workspace = self.init_workspace()
        self.prepare_sources(workspace)
        self.prepare_ledger(workspace)
        self.prepare_capability(workspace)
        route = json.loads((workspace / "route.json").read_text(encoding="utf-8"))
        route.update({"primary_mode": "research-mentor", "supporting_modes": [], "reviewed": True})
        (workspace / "route.json").write_text(json.dumps(route, indent=2) + "\n", encoding="utf-8")
        run_script("validate_evidence_ledger.py", str(workspace))
        run_script("assemble_skill.py", str(workspace))
        package = workspace / "output" / "test-researcher-skill"
        result = run_script("validate_distillation_package.py", str(package), "--json")
        self.assertEqual(json.loads(result.stdout)["achieved_tier"], "v2")
        dist = self.root / "dist"
        run_script("package_skill.py", str(package), "--output", str(dist))
        archive = dist / "test-researcher-skill.zip"
        self.assertTrue(archive.is_file())
        with zipfile.ZipFile(archive) as handle:
            self.assertIn("test-researcher-skill/SKILL.md", handle.namelist())

    def test_v3_requires_all_reviewed_tests(self) -> None:
        workspace = self.init_workspace(tier="v3")
        self.prepare_sources(workspace)
        self.prepare_ledger(workspace)
        self.prepare_capability(workspace)
        route = json.loads((workspace / "route.json").read_text(encoding="utf-8"))
        route.update({"primary_mode": "research-mentor", "supporting_modes": [], "reviewed": True})
        (workspace / "route.json").write_text(json.dumps(route, indent=2) + "\n", encoding="utf-8")
        run_script("assemble_skill.py", str(workspace))
        package = workspace / "output" / "test-researcher-skill"
        run_script("validate_distillation_package.py", str(package), expect=2)
        cases = [{"id": f"T-{kind}", "type": kind, "prompt": f"{kind} test"} for kind in (
            "known", "forward", "contrast", "boundary", "adversarial"
        )]
        (package / "tests" / "test-cases.jsonl").write_text(
            "".join(json.dumps(case) + "\n" for case in cases),
            encoding="utf-8",
        )
        report = {
            "schema_version": 1,
            "reviewed": True,
            "tests": [
                {"id": case["id"], "type": case["type"], "status": "pass", "reviewed": True}
                for case in cases
            ],
            "notes": [],
        }
        (package / "validation" / "report.json").write_text(
            json.dumps(report, indent=2) + "\n",
            encoding="utf-8",
        )
        result = run_script("validate_distillation_package.py", str(package), "--json")
        self.assertEqual(json.loads(result.stdout)["achieved_tier"], "v3")

    def test_update_rule_blocks_contradiction(self) -> None:
        workspace = self.init_workspace()
        for task_id, outcome in (("task-a", "support"), ("task-b", "support"), ("task-c", "contradict")):
            run_script(
                "update_rule.py", "add", str(workspace),
                "--rule-id", "H-001", "--task-id", task_id, "--outcome", outcome,
            )
        run_script("update_rule.py", "evaluate", str(workspace), "--rule-id", "H-001", expect=3)


if __name__ == "__main__":
    unittest.main()
