# Profile: lightweight

**Machine-readable definition:** [`../lightweight.yaml`](../lightweight.yaml)

**Skill count:** 6

---

## When to Choose This Profile

Choose this profile when the guardrails need to be light but the two failure modes that matter most — false completion claims and silently dropped work — must still be prevented.

Typical situations:

- Small scripts and one-off utilities.
- Exploratory work where the shape of the solution is not settled yet.
- A personal project with no other consumers.
- A first step into agent engineering standards, before committing to the full set.

## What This Profile Enforces

- The task is identified and scoped before execution, and unrelated operations are not added.
- Every user message is classified before acting; a question is answered before anything is executed, and a message arriving mid-task interrupts the autonomous workflow.
- Tests are actually executed, and results are reported as PASS, FAIL, BLOCKED, NOT_RUN, or NOT_APPLICABLE.
- Unfinished work is recorded instead of being silently dropped or described as complete.
- Explicitly specified operations, paths, and file scopes are followed literally, without unauthorized reinterpretation or expansion.
- Nothing published to a public repository identifies a person, an organization, an internal system, or the tool that produced it.

## What This Profile Omits

Everything else. In particular, there is no requirement for interface contracts, code asset inventory, data audit, structured logging, or documentation. A small change does not need a contract, and repeating a five-line helper in a throwaway script is not the problem this profile exists to solve.

Use this profile as a starting point, and move to `development` or `full-engineering` when the project's needs grow.

## Install

```bash
python3 scripts/install.py --agent claude-code --profile lightweight
```
