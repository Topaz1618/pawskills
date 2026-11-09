# Profile: development

**Machine-readable definition:** [`../development.yaml`](../development.yaml)

**Skill count:** 9

---

## When to Choose This Profile

Choose this profile when the agent spends most of its time writing and modifying code in an existing application.

Typical situations:

- Feature work and bug fixes in an existing service.
- Refactoring a module that already has callers.
- A codebase with enough history that duplicating an existing helper is a realistic risk.
- A team that wants change reports and real test results, without the full documentation apparatus.

## What This Profile Enforces

- The task is classified before execution; checks scale with the size of the change.
- Existing modules and functions are inspected before a new implementation is written.
- New or modified modules have a defined input contract, output contract, and invocation contract.
- Logs record what actually happened, including failures and fallback paths.
- Tests are actually executed and results are reported honestly.
- Existing functionality is checked for regression when an interface changes.
- Every change is delivered with a file-level and function-level report.
- Work discovered but not completed is recorded.
- Explicitly specified operations, paths, and file scopes are followed literally, without unauthorized reinterpretation or expansion.

## What This Profile Omits

Data audit and reproducibility, technical documentation, documentation structure, and language expression standards are not included. This profile assumes the agent is not the primary author of long-form documentation, and that data processing is not its main output.

## Install

```bash
python3 scripts/install.py --agent claude-code --profile development
```
