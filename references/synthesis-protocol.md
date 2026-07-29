# Synthesis protocol

Populate `extraction/capability.json`. Every entry must include:

```json
{
  "id": "H-001",
  "statement": "When ..., prefer ... because ...",
  "claim_ids": ["C-001", "C-004"],
  "scope": "...",
  "conditions": "...",
  "failure_conditions": "..."
}
```

## Section requirements

### Knowledge

Represent concepts and relationships. Do not repeat the source index.

### Taste

State criteria that rank alternatives. Include observable indicators of quality.

### Heuristics

Use condition → action/check → reason → failure condition.

### Workflows

Include `title`, `trigger`, `inputs`, `steps`, `outputs`, `stop_conditions`, and `claim_ids`.

### Anti-patterns

Include symptom, likely cause, consequence, repair, and evidence.

### Boundaries

State tasks, scopes, evidence conditions, identity claims, or risk levels where the Skill must stop, qualify, or escalate.

### Limitations

State what the sources cannot reveal: private intent, tacit intuition, failed unpublished work, contributor attribution, temporal change, or domain transfer.

## Synthesis checks

- No entry without accepted/revised claim IDs.
- No generic advice that a baseline model would likely produce unchanged.
- No personality style inside a professional workflow.
- No contradiction silently averaged into a single rule.
- No source quotation required at runtime when a concise evidence-linked rule suffices.
