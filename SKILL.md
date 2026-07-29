---
name: omni-distill
description: Build or update evidence-grounded Agent Skills from people, experts, researchers, document corpora, case sets, project histories, and repeated user feedback. Use when Codex must distill implicit knowledge, research taste, decision heuristics, SOPs, anti-patterns, or a navigable knowledge structure into a traceable, testable, versioned Skill rather than merely summarize source material.
---

# OmniDistill

Convert source material into a capability package. Do not impersonate a person, promote a single observation into a stable rule, or confuse a knowledge summary with an executable Skill.

## Non-negotiable outputs

Produce six capability layers:

1. `Knowledge`: facts, concepts, vocabulary, and relationships.
2. `Taste`: quality criteria, priorities, and evidence standards.
3. `Heuristics`: conditional decision rules.
4. `Workflows`: ordered actions with inputs, outputs, branches, and stop conditions.
5. `Anti-patterns`: recurrent failure modes and repairs.
6. `Boundaries`: scope, uncertainty, attribution, privacy, and identity limits.

Connect every non-trivial rule to a claim in the evidence ledger. Keep persona or voice traits optional and separate from professional capability.

## Phase 0: establish purpose and authority

Before collecting or reading sources, establish:

- the target and intended tasks;
- whether the output is private, internal, or redistributable;
- which materials the user is authorized to process;
- whether identity simulation is excluded, optional, or explicitly requested;
- the requested quality tier.

Do not ingest private messages, email, work records, or third-party personal data without clear authority. Redact secrets and direct identifiers before analysis. Read [source-and-ethics.md](references/source-and-ethics.md) for private, copyrighted, or redistributable inputs.

## Phase 1: initialize and route

Initialize a workspace:

```bash
python scripts/init_distillation_workspace.py \
  --target "Target name" \
  --purpose "Tasks the resulting Skill must perform" \
  --tier v2 \
  --output-root ./workspaces
```

Route the task:

```bash
python scripts/route_modes.py \
  --brief "Distill a professor's papers, interviews, course notes, and lab projects into a research mentor" \
  --output ./workspaces/<slug>/route.json
```

Treat routing as a reviewable recommendation, not an oracle. Read [mode-router.md](references/mode-router.md), then load only the references for selected modes:

- [mode-person-thinking.md](references/mode-person-thinking.md)
- [mode-work-expert.md](references/mode-work-expert.md)
- [mode-research-mentor.md](references/mode-research-mentor.md)
- [mode-corpus.md](references/mode-corpus.md)
- [mode-case-pattern.md](references/mode-case-pattern.md)
- [mode-project-retro.md](references/mode-project-retro.md)
- [mode-self-evolution.md](references/mode-self-evolution.md)

Use multiple modes when the evidence and intended tasks require them. Do not force every mode into every project.

## Phase 2: register sources

Copy or link authorized materials into `sources/raw/`. Register them:

```bash
python scripts/register_sources.py ./workspaces/<slug>
```

Optionally supply a metadata CSV to declare author, date, access level, rights, consent, and attribution:

```bash
python scripts/register_sources.py ./workspaces/<slug> \
  --metadata ./source-metadata.csv
```

Review `sources/source-index.csv`. Unknown rights default to internal analysis only. Metadata and search snippets are discovery evidence, not strong support.

## Phase 3: build the evidence ledger

Extract atomic claims, not vague themes. Use [evidence-protocol.md](references/evidence-protocol.md) and populate `evidence/evidence-ledger.csv`.

Each row must record:

- claim and capability layer;
- source IDs and independent-source count;
- evidence level and recurrence;
- personal/team/coauthor/institution/unknown attribution;
- counterevidence review;
- scope, conditions, and failure conditions;
- confidence, status, and allowed use.

Validate before synthesis:

```bash
python scripts/validate_evidence_ledger.py ./workspaces/<slug>
```

Never mark as a core rule:

- metadata-only or snippet-only evidence;
- speculation or weak inference;
- a one-off preference;
- an unattributed team result presented as an individual's method;
- a success-only correlation presented as a causal recipe.

## Phase 4: synthesize capability

Create `extraction/capability.json` according to [synthesis-protocol.md](references/synthesis-protocol.md). Preserve contradictions and time changes; do not average them away.

Every heuristic should have this shape:

```text
When <conditions>, prefer/check <action> because <reason>.
Do not apply when <failure conditions>.
Evidence: <claim IDs>.
```

Every workflow must specify:

- trigger and required inputs;
- ordered steps;
- decision branches;
- artifacts produced;
- stop/escalation conditions;
- linked claim IDs.

Assemble the generated Skill:

```bash
python scripts/assemble_skill.py ./workspaces/<slug>
```

The assembler refuses unsupported claim links and separates evidence from execution instructions.

## Phase 5: validate behavior

Read [validation-protocol.md](references/validation-protocol.md). Create tests for:

1. `known`: reproduce a documented judgment.
2. `forward`: decide a genuinely new case.
3. `contrast`: compare enabled vs. baseline behavior.
4. `boundary`: stop, qualify, or ask when evidence is insufficient.
5. `adversarial`: resist identity impersonation, false attribution, and unsupported confidence.

Store test definitions in `tests/test-cases.jsonl` and reviewed outcomes in `validation/report.json`.

Validate the package:

```bash
python scripts/validate_distillation_package.py \
  ./workspaces/<slug>/output/<skill-name>
```

The validator computes the achieved tier. Never claim a higher tier than the files and reviewed tests support.

## Phase 6: update without drift

Read [update-protocol.md](references/update-protocol.md). Record feedback as observations:

```bash
python scripts/update_rule.py add ./workspaces/<slug> \
  --rule-id H-001 \
  --task-id task-2026-001 \
  --outcome support \
  --evidence C-014
```

Evaluate promotion eligibility:

```bash
python scripts/update_rule.py evaluate ./workspaces/<slug> --rule-id H-001
```

Use the lifecycle:

```text
observation → candidate → tested → accepted → revised → deprecated
```

Require repeated, cross-task evidence before promotion. Route contradictions to review; never silently overwrite an accepted rule.

## Quality tiers

- `v0 — scaffold`: target, purpose, authority, route, and source inventory exist.
- `v1 — evidenced`: valid ledger, attribution, counterevidence review, and source coverage exist.
- `v2 — operational`: validated heuristics, workflows, anti-patterns, boundaries, and runnable Skill package exist.
- `v3 — validated`: reviewed known, forward, contrast, boundary, and adversarial tests pass; update history and rollback metadata exist.

See [package-spec.md](references/package-spec.md) for exact required files and tier gates.

## Completion rules

Do not say “distillation complete” until:

- the declared tier equals the validator's achieved tier;
- every core rule links to accepted evidence;
- the package states what it cannot know or do;
- the output is distinguishable from a generic model on forward tests;
- private or restricted sources are not redistributed;
- the Skill can be packaged and revalidated from a clean directory.

Package only after validation:

```bash
python scripts/package_skill.py ./workspaces/<slug>/output/<skill-name> --output ./dist
```
