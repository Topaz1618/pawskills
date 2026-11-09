# Terminology

The vocabulary used across the standards in this repository.

Each entry gives the meaning the standard set assigns to a term, what it excludes, and which standard governs it. When an agent uses one of these words, it is making a claim that a reviewer can check.

Terms are listed alphabetically. Terms the repository deliberately does not use are listed at the end, with the reason.

---

## A

### Audit trail
The set of records that lets a human trace a result back to the raw inputs and the processing steps that produced it, without relying on the agent's account.

Excludes: a summary of what happened. A summary is interpretation, not an audit trail.

Governed by `data-audit-reproducibility`.

### Agent
The actor performing development, analysis, or review work. "Agent" and "implementer" are used interchangeably throughout this repository; both mean whoever is producing the work.

Excludes: the person reviewing the work.

---

## B

### Baseline
The minimum set of standards that a project requires, selected as a profile.

Excludes: an ideal target state. A baseline is what is enforced today.

Governed by `task-execution-governance`.

---

## C

### Compatible change
A change that preserves the observable behaviour existing callers depend on. A change is compatible when an existing caller requires no modification and produces the same result.

Excludes: a change that is merely "probably fine". Compatibility is a checkable property.

Governed by `interface-contract`.

### Completion
The state in which the requested work has been performed, verified as far as it could be, and reported accurately — including whatever remains unfinished.

Excludes: code that is written but unverified, and code that is verified but unreported.

Governed by `task-execution-governance`, `testing-verification`, `change-report-delivery`.

### Contract
The declared input shape, output shape, failure behaviour, invocation method, and compatibility rules of an interface.

Excludes: a convention that is followed in practice but written nowhere.

Governed by `interface-contract`.

---

## D

### Data lineage
The chain of provenance from a source, through each transformation, to a final output.

Excludes: a data-flow diagram of the code. Lineage is about data instances, not program structure.

Governed by `data-audit-reproducibility`.

### Data-first execution
Executing a step only for the portion of data that is actually missing, after confirming that the existing data is already adequate for the rest.

Excludes: re-running a complete pipeline because running it is simpler than checking what already exists.

Governed by `data-first-execution`.

---

## E

### Evidence
An artifact that can be inspected independently: a file, a log, a test report, a data record, a command output.

Excludes: the agent's assertion that the evidence exists. Asserting is not evidencing.

Governed by `engineering-transparency`, `testing-verification`.

### Explicit instruction
A user-specified operation, scope, path, method, or constraint that the agent is required to execute literally.

Excludes: an inferred objective, and a general permission to do good work.

Governed by `explicit-instruction-fidelity`.

---

## F

### Fallback path
An alternate route taken when a primary source or step fails. The use of a fallback is itself an event that must be recorded.

Excludes: silently substituting a default for a failed call.

Governed by `production-logging`.

### Failure
An operation that did not produce its intended result, whether it raised, returned nothing, or returned something incorrect.

Excludes: a caught exception that was handled but not reported.

Governed by `production-logging`, `testing-verification`.

---

## H

### Human auditability
The property that an independent person can inspect the work, verify the claims, and reproduce the result without asking the agent for an explanation.

Excludes: a clear explanation from the agent. A good explanation is not auditability.

Governed by `engineering-transparency`, `technical-documentation`.

---

## I

### Increment
The smallest unit of work that can be independently verified, added and checked before the next is started.

Excludes: a batch of related edits that can only be evaluated together.

Governed by `task-execution-governance`.

### Interface
A boundary across which one component passes data or requests to another: a function signature, a CLI contract, an HTTP endpoint, a file format, a message schema.

Excludes: an internal call within one module, which is covered by `engineering-transparency` instead.

Governed by `interface-contract`.

---

## L

### Log
A record of a real event, written at the time it happened, containing the actual values involved.

Excludes: a log that says "loaded successfully" without showing what was loaded, and a log written after the fact from memory.

Governed by `production-logging`.

### Lineage
See **Data lineage**.

---

## M

### Manifest
The installer-written record of which skills Pawskills installed, where, when, and with which file hashes. Used to protect user-modified files during uninstall.

Excludes: a lockfile of dependency versions, and a backup directory.

Governed by `scripts/install.py`.

---

## N

### Normalization
The transformation of parsed data into a consistent schema, without discarding values that are still needed.

Excludes: cleaning. Normalization makes shapes comparable; cleaning removes defects.

Governed by `data-audit-reproducibility`.

---

## O

### Overwrite protection
The rule that an existing skill directory is never replaced without explicit force, and that the previous version is backed up first.

Excludes: a backup that is created after the overwrite.

Governed by `scripts/install.py`.

---

## P

### Profile
A named, machine-readable subset of the standards for a particular working style, declared in `profiles/*.yaml`.

Excludes: a plugin, a preset of configuration, and a version tag.

Governed by `task-execution-governance`.

### Provenance
The origin of a piece of data: where it came from, when it was retrieved, and in what condition.

Excludes: a guess. If the source is unclear it is recorded as unknown.

Governed by `data-audit-reproducibility`.

---

## R

### Raw data
The unmodified content as obtained from its source, stored separately from any processing result.

Excludes: parsed, cleaned, or summarized data. Once a record is transformed, it is no longer raw.

Governed by `data-audit-reproducibility`.

### Reconciliation
The check that counts across processing stages add up: raw count = successfully processed count + failure count.

Excludes: adjusting the reported counts until they balance. The counts are what happened; the arithmetic is a test, not a target.

Governed by `data-audit-reproducibility`, `testing-verification`.

### Reproducibility
The ability to re-run a historical execution and obtain the same result, using the recorded inputs, code version, configuration, and parameters.

Excludes: a claim of universal reproducibility. When external services or models have changed, the limit must be stated.

Governed by `data-audit-reproducibility`.

---

## S

### Scope
The set of files, directories, interfaces, and operations that a task is authorized to touch, established before execution begins.

Excludes: an understanding of what the task "really" requires. Scope comes from the user, not from the agent's judgement of what would be better.

Governed by `task-execution-governance`, `explicit-instruction-fidelity`.

### Standard
One of the instruction documents under `skills/`, addressing one specific agent failure mode, written as direct obligations on the agent.

Excludes: general advice, style guides, and principles documents.

Governed by `task-execution-governance`.

---

## T

### Traceability
The ability to link a reported result back to the code, data, and execution that produced it.

Excludes: a narrative that connects the steps in prose.

Governed by `engineering-transparency`.

### Truthful reporting
Reporting the actual outcome of every operation — including failures, partial runs, skipped verification, and unfinished work — without softening it into a success.

Excludes: reporting only the parts that worked.

Governed by `change-report-delivery`, `unfinished-work-tracking`.

---

## U

### Unfinished work
Any task-relevant item that was identified but not completed, including what it is, what state it is in, and what remains to do.

Excludes: a mental note. Work that is only known to the agent is lost.

Governed by `unfinished-work-tracking`.

---

## V

### Verification
An executed check whose actual result is observed and reported. Verification statuses are `PASS`, `FAIL`, `BLOCKED`, `NOT_RUN`, and `NOT_APPLICABLE`.

Excludes: reasoning that the result would be correct. Only `NOT_RUN` and `NOT_APPLICABLE` describe work that was not performed, and both must be stated explicitly.

Governed by `testing-verification`.

### Version
An identifier that ties a set of files to a specific content state: a tag, a commit, a recorded hash set, or a dated backup directory.

Excludes: "latest", and a branch name without a resolved commit.

Governed by `data-audit-reproducibility`, `scripts/install.py`.

---

## Terms This Repository Does Not Use

| Avoid | Use instead | Reason |
|---|---|---|
| Best practice | Standard | A standard states an obligation; a best practice states a preference and cannot be checked. |
| Simply, just, obviously | — | These words assert that a step is trivial and discourage the checking the standards require. |
| Handle edge cases | Name the case and the behaviour | "Edge case" hides which case is meant and what should happen. |
| As needed | State the condition | "As needed" leaves the trigger undefined and cannot be verified. |
| Optimise / improve | Name the property being changed | "Improve" names no target, so there is nothing to check afterwards. |
| Probably, should be fine | — | An unverified prediction presented as an outcome. |
| Legacy | Historical, retained for compatibility, superseded | "Legacy" implies the code is expendable; often it is still in production. |

---

## Related Documents

- [Engineering Principles](engineering-principles.md) — why the standards exist.
- [Audit Data Model](audit-data-model.md) — the concrete record structures.
- [Task Execution Governance](../skills/task-execution-governance/SKILL.md) — how scope and standards are selected.
