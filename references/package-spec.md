# Package specification and tier gates

## Workspace

```text
workspace/
├── project.json
├── route.json
├── sources/
│   ├── raw/
│   └── source-index.csv
├── evidence/evidence-ledger.csv
├── extraction/capability.json
├── tests/test-cases.jsonl
├── validation/report.json
├── updates/observations.jsonl
├── snapshots/
└── output/<skill-name>/
```

## Generated Skill

```text
<skill-name>/
├── SKILL.md
├── agents/openai.yaml
├── manifest.json
├── references/
│   ├── evidence-ledger.csv
│   ├── knowledge.md
│   ├── taste.md
│   ├── heuristics.md
│   ├── workflows.md
│   ├── anti-patterns.md
│   ├── boundaries.md
│   └── limitations.md
├── sources/source-index.csv
├── tests/test-cases.jsonl
├── validation/report.json
└── updates/history.jsonl
```

## Tier gates

| Tier | Gate |
|---|---|
| v0 | Valid target, purpose, route, identity policy, and source inventory |
| v1 | At least one accepted evidence-linked claim; valid source links and attribution |
| v2 | Non-empty heuristics, workflows, anti-patterns, and boundaries, all linked to accepted claims |
| v3 | Reviewed passing known, forward, contrast, boundary, and adversarial tests; versioned build lineage and rollback support |

The validator reports the achieved tier and rejects overclaiming.
