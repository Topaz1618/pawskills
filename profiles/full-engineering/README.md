# Profile: full-engineering

**Machine-readable definition:** [`../full.yaml`](../full.yaml)

**Skill count:** 14 (all standards)

---

## When to Choose This Profile

Choose this profile when the agent works on a codebase that other people depend on, and when a change that skips documentation, verification, or interface contracts would create real downstream cost.

Typical situations:

- A shared library or service with more than one maintainer.
- A production system where an incorrect claim about test results is more expensive than extra documentation.
- A team that has been bitten by duplicated implementations, undocumented interfaces, or logs that hid failures.
- An onboarding or compliance context where the agent's output is reviewed by someone other than its author.

## What This Profile Enforces

- Every task is scoped before execution; the required checks depend on the size of the change.
- Existing data and existing code are inspected before anything is re-run or re-written.
- New modules have a defined input contract, output contract, and invocation contract.
- Raw data is preserved separately from processed results, and every transformation is recorded.
- Logs record what actually happened, including failures, empty results, and fallback paths.
- Tests are actually executed, and results are classified as PASS, FAIL, BLOCKED, NOT_RUN, or NOT_APPLICABLE.
- Every change is delivered with a file-level and function-level report.
- Work discovered but not completed is recorded rather than silently dropped.
- Technical documentation reflects the actual implementation.
- Explicitly specified operations, paths, and file scopes are followed literally, without unauthorized reinterpretation or expansion.

## Cost

This profile requires the most agent effort. It is the right trade when the cost of an unverified or undocumented change exceeds the cost of producing the verification and documentation.

## Install

```bash
python3 scripts/install.py --agent claude-code --profile full
```
