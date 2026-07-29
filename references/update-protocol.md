# Update protocol

Keep immutable observations and versioned snapshots.

## Promotion

1. Record feedback with rule ID, task ID, outcome, environment, and evidence.
2. Deduplicate repeated reports from the same task.
3. Promote to candidate only after recurrence across at least two tasks.
4. Create a test before promotion to tested.
5. Require review before accepted.
6. Preserve the prior rule and rationale when revising.
7. Deprecate rather than delete obsolete rules.

## Conflict policy

Any contradiction blocks automatic promotion. Determine whether it reflects:

- different scope;
- temporal change;
- different contributor;
- environment change;
- a genuinely false rule.

## Rollback

Before rebuilding an existing package, `assemble_skill.py` snapshots it. Retain:

- previous package;
- previous manifest;
- changed claims;
- reason for update;
- validation delta.
