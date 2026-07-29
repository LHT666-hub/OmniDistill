# Evidence protocol

## Claim granularity

Write one testable proposition per row. Avoid claims such as “values quality” or “thinks deeply.” Prefer: “When benchmark gains are small, requires error analysis before treating the change as meaningful.”

## Evidence ladder

| Level | Meaning | Core-rule eligibility |
|---|---|---|
| `direct` | Source explicitly states or demonstrates the claim | Eligible with scope and review |
| `recurrent` | Independent sources show the same pattern | Preferred |
| `strong-inference` | Multiple indirect signals support it | Candidate/tested, not high confidence |
| `weak-inference` | Limited or ambiguous indirect evidence | Never accepted |
| `speculation` | Exploratory hypothesis | Never accepted |
| `counterevidence` | Challenges or narrows another claim | Required in review |

Metadata, search snippets, titles, and second-hand summaries are discovery aids. They do not support a high-confidence behavioral or methodological claim.

## Independence

Two repetitions are not independent when they:

- repeat the same interview;
- quote the same press release;
- derive from the same project or coauthor group;
- copy one another;
- are multiple versions of the same document.

Use `independence_group` in the source index.

## Confidence

- `high`: direct or recurrent evidence, at least two independent sources, reviewed counterevidence, narrow scope.
- `medium`: plausible pattern with limitations or partial attribution.
- `low`: retain as candidate or question, not executable core behavior.

## Attribution

Use `individual`, `team`, `coauthor`, `institution`, `unknown`, or `not-applicable`. Personal-method claims cannot be accepted with unknown attribution.

## Counterevidence

For every accepted taste, heuristic, or workflow claim:

1. search for explicit exceptions, failures, later changes, and criticism;
2. record counterevidence IDs or record that the search found none;
3. narrow scope when evidence conflicts;
4. reject the rule if its predictive value collapses.

