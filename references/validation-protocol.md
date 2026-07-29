# Validation protocol

Structure checks are necessary but not sufficient. Use reviewed behavioral tests.

## Test types

### Known

Give a source-documented situation without revealing the documented answer. Check whether the Skill reaches a compatible judgment and cites the relevant rule.

### Forward

Give a new but in-scope situation. Check whether the Skill applies a transferable rule rather than recalling wording.

### Contrast

Run the same task with and without the Skill. Compare decision criteria, evidence use, specificity, and boundary handling. Style difference alone does not count.

### Boundary

Use missing, conflicting, out-of-domain, or weak evidence. The Skill should qualify, ask, or stop.

### Adversarial

Request identity impersonation, false certainty, private-belief inference, team-to-person attribution, or success-only causal advice. The Skill should resist.

## Result record

Each result in `validation/report.json` must contain:

- `id` and `type`;
- `status`: `pass`, `fail`, or `inconclusive`;
- `reviewed`: boolean;
- evaluated artifact or stable path;
- criteria and concise evidence;
- reviewer and review date;
- follow-up action.

Do not self-award v3 from model-generated test text. A human or independent evaluation process must review outcomes.
