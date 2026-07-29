---
name: omni-distill
description: Evidence-driven meta skill for distilling people, experts, researchers, documents, successful cases, projects, and interaction histories into executable Skills. Use when the user wants to extract hidden expertise, workflows, decision patterns, research taste, knowledge structures, or personal operating rules from source materials.
---

# OmniDistill

## Overview

OmniDistill is a universal distillation framework. It converts implicit knowledge into an executable Skill package rather than producing a simple summary.

The goal is to preserve:

- what the target knows (Knowledge)
- what the target values (Taste)
- how the target decides (Heuristics)
- how the target works (Workflows)
- what the target avoids (Anti-patterns)
- where inference should stop (Boundaries)

## Core Principle

Do not distill words. Distill reusable capability.

A successful distillation must answer:

1. What evidence supports this rule?
2. Can this rule generate decisions on unseen problems?
3. Is this pattern stable or only a one-time event?

Never confuse:

- summary with skill
- style imitation with expertise
- public information with private beliefs
- successful outcomes with transferable methods

## Workflow

### Phase 1: Identify Distillation Target

Classify the input:

- person thinking
- work expert
- research mentor
- corpus knowledge
- case pattern
- project retrospective
- self evolution
- hybrid

Determine:

- intended usage
- target tasks
- available evidence
- required quality tier

### Phase 2: Build Evidence Ledger

Create a Claim-Evidence ledger.

For each extracted rule record:

- claim
- source
- evidence type
- confidence
- limitations

Evidence levels:

- Direct evidence
- Repeated pattern
- Strong inference
- Weak inference
- Unknown

Do not promote weak inference into core rules.

### Phase 3: Extract Four Layers

Generate four separate layers:

## Knowledge

Facts, concepts, terminology, methods and references.

## Taste

Judgment criteria:

- what is important
- what is high quality
- what evidence matters
- what should be rejected

## Heuristics

Reusable decision rules.

Example:

"When information is incomplete, first check whether the problem definition is wrong before optimizing the solution."

## Workflows

Executable procedures.

Example:

Problem framing → evidence collection → option evaluation → decision → review

### Phase 4: Extract Failure Knowledge

Always search for:

- failures
- rejected ideas
- criticisms
- limitations
- exceptions

A Skill without failure boundaries is incomplete.

### Phase 5: Generate Skill Package

Create:

```
target-skill/
├── SKILL.md
├── references/
│   ├── evidence-ledger.md
│   ├── knowledge-map.md
│   ├── mental-models.md
│   ├── heuristics.md
│   ├── workflows.md
│   ├── anti-patterns.md
│   └── limitations.md
└── sources/
    └── source-index.md
```

SKILL.md should contain execution instructions, not a giant knowledge dump.

### Phase 6: Validation

Run three tests.

## Evidence Test

Are important rules supported by evidence?

## Generation Test

Can the Skill handle new situations not explicitly present in the sources?

## Difference Test

Does enabling the Skill produce better decisions than a normal model?

If not, the distillation only created a summary.

### Phase 7: Continuous Update

New information follows this pipeline:

Single observation → candidate rule → repeated pattern → stable rule

Do not immediately rewrite core principles from one feedback event.

## Output Standard

Every completed distillation should report:

1. Distillation target
2. Evidence coverage
3. Extracted knowledge
4. Mental models
5. Decision heuristics
6. Workflows
7. Anti-patterns
8. Confidence and limitations
9. Validation results
