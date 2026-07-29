# Reference projects and design response

This file records methodological inspiration. OmniDistill is an independent implementation and does not combine third-party code or prose.

| Project | Useful contribution | Limitation addressed by OmniDistill |
|---|---|---|
| [colleague-skill / dot-skill](https://github.com/titanwings/colleague-skill) | Multi-source personal traces; Work Skill + Persona separation | Enforce authority, privacy, context rules, and capability/persona isolation |
| [Nuwa Skill](https://github.com/alchaincyf/nuwa-skill) | Multi-lane public-person research; mental models, heuristics, boundaries | Add ledger-level provenance, conservative identity policy, tier gates |
| [MentorForge](https://github.com/qwqalice/MentorForge) | Full-paper signals, research-operating-system framing, evidence tiers | Add explicit contributor attribution and cross-paradigm research signals |
| [Chinese Grant Writer Skills](https://github.com/HuiyuLi-2000/Chinese-Grant-Writer-Skills) | Examples into executable writing structures and checks | Add negative cases, scope, causal restraint, and anti-template safeguards |
| [Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills) | Guide + executable Skill; staged research workflow | Avoid discipline universalism and pseudo-precision; respect CC BY-NC-SA licensing |
| [Corpus2Skill](https://github.com/dukesun99/Corpus2Skill) | Hierarchical, navigable corpus compilation | Separate navigation from transferable capability |
| [OpenKB](https://github.com/VectifyAI/OpenKB) | Persistent wiki, Skill Factory, validation, history, rollback | Add claim-level evidence and behavioral tier gates |
| [self-improving-agent](https://github.com/peterskoett/self-improving-agent) | Runtime learning logs and promotion to durable instructions | Add cross-task thresholds, contradiction blocks, revision and deprecation |
| [Academic Reference Matcher](https://github.com/keros68/academic-reference-matcher-skill) | Claim–reference matching and evidence-level discipline | Generalize claim–evidence auditing beyond academic citations |

## Shared gaps

Across these approaches, quality can be weakened by one or more of:

- one object type per tool;
- inconsistent evidence thresholds;
- summaries presented as capability;
- success-only evidence;
- personal attribution from team artifacts;
- identity style presented as expertise;
- structural tests without forward or contrast evaluation;
- one-shot generation without governed updates.

OmniDistill treats these as validation failures rather than optional caveats.

