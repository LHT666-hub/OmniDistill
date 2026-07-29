# Mode router

Use the intended task—not merely the source format—to select modes.

| Mode | Primary question | Typical sources | Required capability |
|---|---|---|---|
| `person-thinking` | How does this person frame and decide? | First-person long-form work, interviews, decisions, criticism, timeline | Mental models, heuristics, tensions, boundaries |
| `work-expert` | How is work actually completed? | SOPs, reviews, artifacts, messages, incident records | Procedures, checks, escalation, exception handling |
| `research-mentor` | How are research questions and evidence judged? | Full papers, talks, code, reviews, trajectory | Research taste, method selection, evidence standards |
| `corpus` | What is in the collection and how should it be navigated? | Books, papers, manuals, archives | Knowledge map, topic hierarchy, retrieval routes |
| `case-pattern` | Which patterns recur across successes and failures? | Positive and negative cases with context | Conditional patterns, anti-patterns, scope |
| `project-retro` | Which decisions and constraints explain a project? | Code, commits, ADRs, issues, incidents | Reproduction path, architectural decisions, pitfalls |
| `self-evolution` | Which repeated corrections should become durable rules? | Feedback, errors, repeated preferences | Rule lifecycle, conflict handling, deprecation |

## Composition rules

- Combine `research-mentor + person-thinking` when both scholarly judgment and broader public reasoning matter.
- Add `corpus` when the sources exceed what can be inspected directly in one context.
- Combine `work-expert + project-retro` for operational handover.
- Add `self-evolution` only when repeated observations across tasks exist.
- Keep `case-pattern` separate from causal claims unless the evidence design supports causality.

## Conflict resolution

When modes conflict:

1. Preserve the task-specific rule in its mode.
2. Narrow its scope.
3. Record the conflicting source or counterexample.
4. Prefer observed decisions over promotional language.
5. Prefer a later dated rule only when the target demonstrably changed.

