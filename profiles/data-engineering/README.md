# Profile: data-engineering

**Machine-readable definition:** [`../data.yaml`](../data.yaml)

**Skill count:** 10

---

## When to Choose This Profile

Choose this profile when the agent's main output is data: collection, parsing, transformation, analysis, or reporting.

Typical situations:

- A data pipeline that must be re-runnable by someone else six months later.
- A research or analysis workflow where the conclusion must be traceable to real input data.
- A collection job whose raw responses need to be preserved for audit.
- A team that needs to answer "where did this number come from?" without asking the agent that produced it.

## What This Profile Enforces

- Existing data and historical results are checked before any re-collection or recomputation.
- Every user message is classified before acting; a question is answered before anything is executed, and a message arriving mid-task interrupts the autonomous workflow.
- Incremental execution only: only the missing portion is added, never the whole dataset.
- Raw data is stored separately from processed data, with source, time, hash, and size recorded.
- Every significant transformation records its inputs, outputs, rules, and record counts.
- Record counts reconcile: raw count = processed count + failure count.
- Logs record the real request, the real response, and any fallback path that was taken.
- A failed primary source followed by a successful fallback is visible in the logs, not collapsed into "loaded successfully".
- Tests cover data counts, field structure, and empty-result behavior.
- Deliverables include real data samples, not fabricated ones.
- Unfinished data work is recorded.
- Explicitly specified operations, paths, and file scopes are followed literally, without unauthorized reinterpretation or expansion.
- Nothing published to a public repository identifies a person, an organization, an internal system, or the tool that produced it.

## What This Profile Omits

Interface contract, code asset inventory, technical documentation, documentation structure, and language expression standards are not included. If the agent is also writing and maintaining code that others call, use the `full-engineering` profile instead.

## Install

```bash
python3 scripts/install.py --agent claude-code --profile data
```
